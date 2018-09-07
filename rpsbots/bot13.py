# testing out new strategies
# Name: zai_all_mix_meta
# AUthor: zdg
# Email: rpscontest.b73@gishpuppy.com
# the email is disposable in case it gets spammed
#
# the base strategy is to mix multiple strategies together instead of switching
# then on top of that, switches on the 6 meta strategies
# gets beaten by more adaptive bots like zai_ghpm7all_switch_meta
# but hopefully is more effective against less complex bots

# --------------------- initialization -----------------------------
if not input:
	import random, collections, math

	# micro-optimizations
	rchoice = random.choice
	randint = random.randint
	runit = random.random
	log = math.log
	sqrt = math.sqrt

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

	def pick_max(vec):
		max_val = max(vec)
		max_list = [i for i in range(len(vec)) if vec[i] == max_val]
		return rchoice(max_list)

	def pick_weighted(vec):
		total = sum(vec) + 0.0
		u = runit() * total
		acc = 0.0
		for i in range(len(vec)):
			acc += vec[i]
			if u < acc:
				return i
		else:
			return randint(0, len(vec)-1)

	# calculate the hand with the best expected value against the given op hand
	# random only in case of ties
	def expected(vec):
		expected_payoffs = [vec[S] - vec[P], vec[R] - vec[S], vec[P] - vec[R]]
		max_expected = max(expected_payoffs)
		max_list = [i for i in range(3) if expected_payoffs[i] == max_expected]
		return rchoice(max_list)

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

		def update(self, next_val, up_val):
			self.hist.append(next_val)
			# update the history, order 0 as a special case
			up_ix = 0
			self.contexts[0] = up_val

			# start the prediction with the zeroth order
			self.pred = self.contexts[0]

			# update the higher orders and prediction
			elems = len(self.hist)
			for order in range(1, self.ORDER+1 if elems > self.ORDER else elems):
				pred_ix = up_ix * self.BASE + next_val

				up_ix += self.hist[-order-1] * self.powers[order]
				self.contexts[up_ix] = up_val

				try_get = self.contexts[pred_ix]
				if try_get is not None:
					self.pred = try_get

	# more specific globals
	STRATEGIES = range(27)
	my_ghpm = GHPM(6, 3)
	op_ghpm = GHPM(6, 3)
	both_ghpm = GHPM(6, 9)

	DECAY = 0.98
	sscores = [0 for _ in STRATEGIES]
	rev_sscores = [0 for _ in STRATEGIES]
	next_hands = [None for _ in STRATEGIES]

	PERIOD = 1
	META_DECAY = 0.98
	META_STRATEGIES = range(6)
	meta_sscores = [0 for _ in META_STRATEGIES]
	meta_next = [None for _ in META_STRATEGIES]
	meta_pick = 0

	# SWITCH_DECAY = 0.98
	# switch_scores = [0,0]

	# constant bot
	next_hands[0] = R

	# first hand is completely random - no reason to do otherwise
	output = tr[rchoice(RPS)]

	# bookkeeping
	hands = 1
	last_ix = 0
	score = 0
# --------------------- turn -----------------------------
else:
	last_my = tr[output]
	last_op = tr[input]
	last_payoff = sub[last_my][last_op]

	# update the history matchers
	my_ghpm.update(enc1[last_my], last_ix)
	op_ghpm.update(enc1[last_op], last_ix)
	both_ghpm.update(enc2[last_my][last_op], last_ix)

	if hands > 1:
		# update the scores
		for i in STRATEGIES:
			sscores[i] *= DECAY
			# sscores[i] += pts[sub[next_hands[i]][last_op]]
			sscores[i] += near[sub[next_hands[i]][last_op]]

			rev_sscores[i] *= DECAY
			# rev_sscores[i] += pts[sub[next_hands[i]][last_my]]
			rev_sscores[i] += near[sub[next_hands[i]][last_my]]

		for i in META_STRATEGIES:
			meta_sscores[i] *= META_DECAY
			meta_sscores[i] += pts[sub[meta_next[i]][last_op]]

	# update next_hands
	# constant needs no update

	# use only last
	next_hands[3] = last_my
	next_hands[6] = last_op

	# the bigger strategies
	both_hist = both_ghpm.hist

	pred_op, pred_my = dec2[both_hist[my_ghpm.pred]]
	next_hands[9] = pred_op
	next_hands[12] = pred_my

	pred_op, pred_my = dec2[both_hist[op_ghpm.pred]]
	next_hands[15] = pred_op
	next_hands[18] = pred_my

	pred_op, pred_my = dec2[both_hist[both_ghpm.pred]]
	next_hands[21] = pred_op
	next_hands[24] = pred_my

	# the other indices are just based on the hands at the multiples of 3
	for i in STRATEGIES:
		if i % 3 != 0:
			next_hands[i] = beats[next_hands[i-1]]

	# predict next op
	next_prob = [0, 0, 0]
	for i in STRATEGIES:
		next_prob[next_hands[i]] += sscores[i]
	# next_my = pick_max(next_prob)
	# next_my_weighted = beats[pick_weighted(next_prob)]
	next_my = expected(next_prob)

	# predict next my
	rev_next_prob = [0, 0, 0]
	for i in STRATEGIES:
		rev_next_prob[next_hands[i]] += rev_sscores[i]
	rev_next_my = expected(rev_next_prob)

	# update meta
	meta_next[0] = next_my
	meta_next[3] = rev_next_my
	for i in META_STRATEGIES:
		if i % 3 != 0:
			meta_next[i] = beats[meta_next[i-1]]

	meta_pick = pick_max(meta_sscores)

	meta_next_my = meta_next[meta_pick]

	output = tr[meta_next_my]
	# output = tr[next_my]

	# bookkeeping
	hands += 1
	last_ix += 1
	score += pts[last_payoff]

	# if hands % 100 == 0:
		# print PERIOD
		# print '-' * 80
		# print META_DECAY
