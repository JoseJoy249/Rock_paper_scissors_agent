# Name: zai_mix_markov1_bayes
# Author: zdg
# Email: rpscontest.b73@gishpuppy.com
# the email is disposable in case it gets spammed
#
# let's try out some bayes inference with 1-st order markov model wrappers on
#    various strategies as the hypotheses
# uses approximate bayes inference i.e. weighted hypotheses by likelihood
# also have some ad-hoc decay which helps a lot

# --------------------- initialization -----------------------------
if not input:
	import random, collections, math

	# micro-optimizations
	rchoice = random.choice
	log = math.log
	exp = math.exp

	# global constants and maps
	# using lists and dictionaries because function call and arithmetic is slow
	R, P, S = 0, 1, 2
	RPS = [R, P, S]
	T, W, L = R, P, S
	PAYOFFS = RPS
	tr = {'R':R, 'P':P, 'S':S, R:'R', P:'P', S:'S'}
	sub = [[T, L, W], [W, T, L], [L, W, T]]
	add = [[R, P, S], [P, S, R], [S, R, P]]
	ties, beats, loses = add[T], add[W], add[L]

	pts = [0, 1, -1]
	near = [1, 0, 0]

	enc1 = [1,2,3]
	dec1 = [None, R, P, S]

	enc2 = [[1,2,3], [4,5,6], [7,8,9]]
	dec2 = [None,(R,R),(R,P),(R,S),(P,R),(P,P),(P,S),(S,R),(S,P),(S,S)]

	seed = rchoice(RPS)

	def pick_max(vec):
		max_val = max(vec)
		max_list = [i for i in range(len(vec)) if vec[i] == max_val]
		return rchoice(max_list)

	# calculate the hand with the best expected value against the given op hand
	# random only in case of ties
	def expected(vec):
		expected_payoffs = [vec[S] - vec[P], vec[R] - vec[S], vec[P] - vec[R]]
		max_expected = max(expected_payoffs)
		max_list = [i for i in RPS if expected_payoffs[i] == max_expected]
		return rchoice(max_list)

	def normalize(vec):
		factor = 1.0 / sum(vec)
		for i in range(len(vec)):
			vec[i] *= factor

	def normalized(vec):
		factor = 1.0 / sum(vec)
		return [v * factor for v in vec]

	# greedy history pattern matcher
	# ORDER is the largest context size
	# BASE is the base of the numerical encoding
	# encodes sequences of numbers from 1...BASE as a BASE-adic number
	# encodes the empty sequence as 0
	# apparently this encoding is called a bijective base-BASE system on wikipedia
	class GHPM:
		def __init__(self, ORDER, BASE):
			self.ORDER = ORDER
			self.BASE = BASE
			self.powers = [0] + [BASE ** i for i in range(ORDER)]
			self.hist = []
			self.contexts = collections.defaultdict(lambda: None)
			self.pred = None
			self.preds = [None] * (ORDER+1)

		def update(self, next_val, up_fun):
			self.hist.append(next_val)
			# update the history, order 0 as a special case
			up_ix = 0
			self.contexts[0] = up_fun(self.contexts[0])

			# start the prediction with the zeroth order
			self.pred = self.contexts[0]

			# update the higher orders and prediction
			elems = len(self.hist)
			for order in range(1, self.ORDER+1 if elems > self.ORDER else elems):
				pred_ix = up_ix * self.BASE + next_val

				up_ix += self.hist[-order-1] * self.powers[order]
				self.contexts[up_ix] = up_fun(self.contexts[up_ix])

				try_get = self.contexts[pred_ix]
				self.preds[order] = try_get
				if try_get is not None:
					self.pred = try_get

	class ConstantBot:
		def __init__(self, h, reversed=False):
			self.pred = h

		def update(self, op_hist, my_hist):
			pass

	class LastBot:
		def __init__(self, h, reversed=False):
			self.pred = h
			self.reversed = reversed

		def update(self, op_hist, my_hist):
			self.pred = op_hist[-1] if not self.reversed else my_hist[-1]

	# doesn't update wrapped ghpm
	class GHPMBot:
		def __init__(self, h, ghpm, reversed=False):
			self.pred = h
			self.ghpm = ghpm
			self.reversed = reversed

		def update(self, op_hist, my_hist):
			self.pred = (op_hist if not self.reversed else my_hist)[self.ghpm.pred]

	# this wraps around a deterministic bot using 0-th order markov (counts)
	class Markov0Hypothesis:
		def __init__(self, bot, decay, reversed=False):
			self.reversed = reversed
			# uniform prior
			self.pred_diff_dist = [1.0] * 3
			self.pred_dist_norm = [1.0 / 3.0] * 3
			self.recency_factor = 1.0 / decay
			self.counting_weight = 1.0

			# wraps over a deterministic bot
			self.bot = bot

		def update(self, op_hist, my_hist):
			if self.reversed:
				op_hist, my_hist = my_hist, op_hist
			# update probabilities for last time
			last_diff = sub[op_hist[-1]][self.bot.pred]

			self.counting_weight *= self.recency_factor
			self.pred_diff_dist[last_diff] += self.counting_weight

			# update wrapped bot
			self.bot.update(op_hist, my_hist)

			# predict next distribution
			pred_dist_norm = [None] * 3
			for d in PAYOFFS:
				pred_dist_norm[add[d][self.bot.pred]] = self.pred_diff_dist[d]
			self.pred_dist_norm = normalized(pred_dist_norm)

	# wraps around a deterministic bot using 1-st order markov
	# uses last op and last payoff
	class Markov1Hypothesis:
		def __init__(self, bot, decay, reversed=False):
			self.reversed = reversed
			# uniform prior
			self.pred_diff_matrix = [[3.0] * 3 for _ in range(9)]
			self.pred_dist_norm = [1.0 / 3.0] * 3
			self.recency_factor = 1.0 / decay
			self.counting_weight = 1.0

			# wraps over a deterministic bot
			self.bot = bot
			self.diffs = []

		def update(self, op_hist, my_hist):
			if self.reversed:
				op_hist, my_hist = my_hist, op_hist

			# update diffs for last time
			self.diffs.append(sub[op_hist[-1]][self.bot.pred])

			# update matrix for last time
			self.counting_weight *= self.recency_factor
			if hands >= 2:
				last_last_diff, last_diff = self.diffs[-2], self.diffs[-1]
				last_last_payoff = sub[my_hist[-2]][op_hist[-2]]
				last_last_state = enc2[last_last_diff][last_last_payoff]-1
				self.pred_diff_matrix[last_last_state][last_diff] += self.counting_weight

			# update underlying bot
			self.bot.update(op_hist, my_hist)

			# use first order markov to calculate next diff distribution
			pred_dist_norm = [None] * 3
			last_diff = self.diffs[-1]
			last_payoff = sub[my_hist[-1]][op_hist[-1]]
			last_state = enc2[last_diff][last_payoff]-1
			for d in PAYOFFS:
				pred_dist_norm[add[d][self.bot.pred]] = self.pred_diff_matrix[last_state][d]
			self.pred_dist_norm = normalized(pred_dist_norm)

	# mixes multiple hypotheses together
	class BayesMixer:
		def __init__(self, hypotheses, decay, reversed=False):
			self.reversed = reversed
			# uniform prior
			self.pred_dist_norm = [1.0 / 3.0] * 3
			self.decay_factor = decay
			self.pred = expected(self.pred_dist_norm)

			self.hypotheses = hypotheses
			self.range = range(len(hypotheses))

			# log (P ( history | bot))
			self.log_data_probs = [0.0 for _ in self.hypotheses]

		def update(self, op_hist, my_hist):
			if self.reversed:
				op_hist, my_hist = my_hist, op_hist
			# update probabilities for last time
			for i in self.range:
				data_prob = self.hypotheses[i].pred_dist_norm[op_hist[-1]]
				self.log_data_probs[i] *= self.decay_factor
				self.log_data_probs[i] += log(data_prob)

			# update hypotheses
			for h in self.hypotheses:
				h.update(op_hist, my_hist)

			# approximate likelihoods
			max_factor = max(self.log_data_probs)

			# P ( bot | history ) =  P ( history | bot) * (some normalizing factor)
			likelihoods = [exp(p - max_factor) for p in self.log_data_probs]

			# mix according to likelihood
			pred_dist_norm = [0.0, 0.0, 0.0]
			for i in self.range:
				for h in RPS:
					pred_dist_norm[h] += self.hypotheses[i].pred_dist_norm[h] * likelihoods[i]

			self.pred_dist_norm = normalized(pred_dist_norm)
			self.pred = expected(self.pred_dist_norm)

	# 1st order transition matrix
	# use both last diff and last payoff for each bot
	# markov1 = [[[3.0, 3.0, 3.0] for _ in range(9)] for _ in BOTS]

	# initialize history matching strategies
	my_ghpm = GHPM(6, 3)
	op_ghpm = GHPM(6, 3)
	both_ghpm = GHPM(6, 9)

	# initialize deterministic bots
	constant_bot = ConstantBot(seed)
	last_op_bot = LastBot(seed)
	last_my_bot = LastBot(seed, reversed=True)

	op_ghpm_bot = GHPMBot(seed, op_ghpm)
	rev_op_ghpm_bot = GHPMBot(seed, op_ghpm, reversed=True)

	my_ghpm_bot = GHPMBot(seed, my_ghpm)
	rev_my_ghpm_bot = GHPMBot(seed, my_ghpm, reversed=True)

	both_ghpm_bot = GHPMBot(seed, both_ghpm)
	rev_both_ghpm_bot = GHPMBot(seed, both_ghpm, reversed=True)

	bots = [
		constant_bot, last_op_bot, last_my_bot,
		op_ghpm_bot, rev_op_ghpm_bot, my_ghpm_bot, rev_my_ghpm_bot,
		both_ghpm_bot, rev_both_ghpm_bot
	]

	# initialize the hypotheses
	hypotheses = [Markov1Hypothesis(b, 0.98) for b in bots]

	# initialize bayes mixer
	bayes_mixer = BayesMixer(hypotheses, 0.98)
	# orig_modified = Markov1Hypothesis(bayes_mixer, 0.98)

	mixer = bayes_mixer

	# first hand is completely random - no reason to do otherwise
	next_hand = expected(mixer.pred_dist_norm)
	output = tr[next_hand]

	# bot_diffs = [[] for _ in BOTS]
	# bot_payoffs = [[] for _ in BOTS]

	# bookkeeping
	op_hist = []
	my_hist = []
	hands = 1
	last_ix = 0
	score = 0
# --------------------- turn -----------------------------
else:
	last_op = tr[input]
	last_my = tr[output]
	last_payoff = sub[last_my][last_op]
	op_hist.append(last_op)
	my_hist.append(last_my)

	# update the history matchers
	my_ghpm.update(enc1[last_my], lambda _:last_ix)
	op_ghpm.update(enc1[last_op], lambda _:last_ix)
	both_ghpm.update(enc2[last_op][last_my], lambda _:last_ix)

	mixer.update(op_hist, my_hist)

	next_hand = expected(mixer.pred_dist_norm)

	output = tr[next_hand]

	# bookkeeping
	hands += 1
	last_ix += 1
	score += pts[last_payoff]

	# if hands % 100 == 0:
	# if hands < 10:
		# print