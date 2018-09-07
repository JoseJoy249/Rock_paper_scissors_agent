#uses stuff from http://www.ofb.net/~egnor/iocaine.html
#hist() matcher code, final metastrat. selector, quintuple henny influenced by momo's 'galton' bot
#deeper search in hist_fwd_rvr, also a better reward system to prevent quick metastrat. switching
#freq. predictors try not to win, but to mitigate damage
#licatj @ no-spam-pls rpi.edu

import random
from collections import defaultdict

wins = ['RS','SP','PR']
encode = {'RR':'a', 'RP':'b', 'RS':'c', 'PR':'d', 'PP':'e', 'PS':'f', 'SR':'g', 'SP':'h', 'SS':'i'}
decode = {'a':'RR', 'b':'RP', 'c':'RS', 'd':'PR', 'e':'PP', 'f':'PS', 'g':'SR', 'h':'SP', 'i':'SS', 'x':'XX'}

numMeta = 3 #num of meta strategies for each predictor

if input=='': #first round; initialize everything
	output = input = random.choice('RPS')
	currSet = 0
	score = 0
	lastStratChosen = -2
	allMoves = '' #history of all moves made
	myMoves = ''
	hisMoves = ''

	#initialize strategies
	def alwaysRock():
		return 'R'
	def alwaysPaper():
		return 'P'
	def alwaysScissors():
		return 'S'
	def rand():
		return random.choice('RPS')

	def hist_fwd_rvr(allMoves):
		numToCheck = 2 #numer of matches at each end to look for
		toReturn = []#random.choice('abcdefghi')

		lam = len(allMoves)
		maxDepth = 100
		maxLength = 6
		lastStartF = 0
		lastStartR = lam-1
		l = min(maxLength,lam-1)
		#search forwards strings of decreasing length
		for i in range(numToCheck):
			foundAt = -1
			while l>0 and foundAt==-1:
				foundAt = allMoves.find(allMoves[lam-l:lam],lastStartF,lam-1)
				if foundAt == -1:
					l -= 1
			if foundAt != -1:
				lastStartF = foundAt+l
				toReturn += [allMoves[lastStartF]]
			else:
				lastStartF = lam
				toReturn += ['x']

			#search backwards strings of decreasing length
			foundAt = -1
			while l>0 and foundAt==-1:
				foundAt = allMoves.rfind(allMoves[lam-l:lam],0,lastStartR)
				if foundAt == -1:
					l -= 1
			if foundAt != -1:
				lastStartR = foundAt+l-1
				toReturn += allMoves[foundAt+l]
			else:
				lastStartF = 0
				toReturn += ['x']
		#print toReturn
		return toReturn

	stored = ''
	def histFAll1():
		global allMoves,stored
		stored = hist_fwd_rvr(allMoves)
		return decode[stored[0]][0]
	def histFAll2():
		global stored
		return decode[stored[0]][1]
	def histRAll1():
		global stored
		return decode[stored[1]][0]
	def histRAll2():
		global stored
		return decode[stored[1]][1]
	def histFAll3():
		global stored
		return decode[stored[2]][0]
	def histFAll4():
		global stored
		return decode[stored[2]][1]
	def histRAll3():
		global stored
		return decode[stored[3]][1]
	def histRAll4():
		global stored
		return decode[stored[3]][1]

	histAnalysis = defaultdict(list)
	considerLengths = [3,4]
	histResults = ['']*len(considerLengths)
	def hist(allMoves,considerLengths):
		global histAnalysis,histResults
		lam = len(allMoves)-1
		#learn from previous example
		keys = []
		for l in considerLengths:
			if lam < l: #can't learn this history
				keys.append('')
				continue
			key = allMoves[-l-1:-1]
			histAnalysis[key] += [allMoves[-1]]
			keys.append(key)
		#make predictions
		for i in range(len(considerLengths)):
			if lam < considerLengths[i]: #key will not be valid
				histResults[i] = random.choice('abcdefghi')
				continue
			cand = histAnalysis[keys[i]]
			k = range(len(cand))
			#skew toward more recent ones
			histResults[i] = cand[max(random.choice(k),random.choice(k))]

	#does history matching of length 3 (or whatever considerLengths[0] is)
	def hist1_1():
		global allMoves,considerLengths,histResults,decode
		hist(allMoves,considerLengths)
		return decode[histResults[0]][0]
	#history matching of length 3 (or whatever considerLenghts[0] is), but assumes they're using predictor against you
	def hist1_2():
		global histResults,decode
		return decode[histResults[0]][1]
	def hist2_1():
		global histResults,decode
		return decode[histResults[1]][0]
	def hist2_2():
		global histResults,decode
		return decode[histResults[1]][1]

	frq = [0,0,0]
	def freq1(): #predicts they will make the move they make most often
		global allMoves,frq,decode
		#learn from last move made
		if len(allMoves)==0:
			return 'X'
		frq[ 'RPS'.index(decode[allMoves[-1]][1]) ] += 1
		util = [frq[2]-frq[1],frq[0]-frq[2],frq[1]-frq[0]]
		return 'RPS'[util.index(max(util))]

	frq2 = [0,0,0]
	def freq2(): #like freq, but assumes they think we're playing with freq and they want to beat it
		global allMoves,frq2,decode
		#learn from last move made
		if len(allMoves)==0:
			return 'X'
		frq2[ 'RPS'.index(decode[allMoves[-1]][0]) ] += 1
		util = [frq2[2]-frq2[1],frq2[0]-frq2[2],frq2[1]-frq2[0]]
		return 'PSR'[util.index(max(util))]


	allStrats = [freq1,freq2,hist1_1,hist1_2,hist2_1,hist2_2,histFAll1,histRAll1]
	allStrats += [histFAll2,histRAll2,histFAll3,histRAll3,histFAll4,histRAll4,rand]
	allScores = [0]*len(allStrats)*numMeta
	allPredictions = ['X']*len(allStrats)*numMeta
	#for metameta level:
	mmScor = 0
	mmPred = 'X'
else:
	allMoves = allMoves + encode[output + input]
	myMoves = myMoves + output
	hisMoves = hisMoves + input
	scoreChange = 0
	if (output+input) in wins:
		score += 1
		scoreChange = 1
	elif (input+output) in wins:
		score -= 1
		scoreChange = -1

	if currSet >= 500 and score < 0:
		output = 'X'#don't-know choice, taken care of later
	else: #actually try something
		beat = {'R':'P', 'P':'S', 'S':'R', 'X':'X'}#random.choice('RPS')}
		for i in range(len(allStrats)):
			nmi = numMeta*i
			for j in range(nmi, nmi+3):
				allScores[j] *= 0.85#max(0,allScores[j]-1) #decay
				if allPredictions[j] == input:
					allScores[j] += 5
				elif allPredictions[j] == beat[input]:
					allScores[j] -= 5
			predBase = allStrats[i]() #update predictions:
			jumpUp = {'R':'S', 'P':'R', 'S':'P', 'X':'X'}#random.choice('RPS')}
			allPredictions[nmi] = predBase #P.0 : assume they'll follow the move exactly predicted
			allPredictions[nmi+1] = jumpUp[predBase] #P.1 - assume they predict we'll try to beat predBase
			allPredictions[nmi+2] = jumpUp[jumpUp[predBase]] #P.2 - assume they predict we'll try to beat jumpUp[predBase]

		#for meta meta
		mmScor *= 0.85 #decay
		if mmPred == input:
			mmScor += 3
		elif mmPred == beat[input]:
			mmScor -= 3
		if lastStratChosen != -2:
			if lastStratChosen == -1:
				mmScor += scoreChange
			else:
				allScores[lastStratChosen] += scoreChange
		mx = max(allScores)
		i = random.choice([j for j in range(len(allScores)) if allScores[j]==mx])
		output = beat[allPredictions[i]]
		lastStratChosen = i
		mmPred = beat[output]
		if mmScor > allScores[i]:
			output = mmPred
			lastStratChosen = -1

	if output=='X':
		if len(allMoves) > 2:
			#use triple henny, from momo's 'galton' bot and http://webdocs.cs.ualberta.ca/~darse/rsbpc.html
			choices = []
			for h in range(5):
				choices.append(decode[allMoves[random.randint(0,len(allMoves))-1]][1])
			output = beat[random.choice(choices)]
		else:
			output = random.choice('RPS')

currSet += 1
