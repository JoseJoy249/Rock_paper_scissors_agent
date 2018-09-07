# See http://overview.cc/RockPaperScissors for more information about rock, paper, scissors
# Extension to bayes 9: Also look at only opp and only my moves

from collections import defaultdict
import operator
import random

if input == "":
  score = {'RR': 0, 'PP': 0, 'SS': 0, 'PR': 1, 'RS': 1, 'SP': 1,'RP': -1, 'SR': -1, 'PS': -1,}
  cscore = {'RR': 'r', 'PP': 'r', 'SS': 'r', 'PR': 'b', 'RS': 'b', 'SP': 'b','RP': 'c', 'SR': 'c', 'PS': 'c',}
  beat = {'P': 'S', 'S': 'R', 'R': 'P'}
  cede = {'P': 'R', 'S': 'P', 'R': 'S'}
  rps = ['R', 'P', 'S']

  def counter_prob(probs):
    weighted_list = []
    for h in ['R', 'P', 'S']:
      weighted = 0
      for p in probs.keys():
        points = score[h+p]
        prob = probs[p]
        weighted += points * prob
        weighted_list.append((h, weighted))

    return max(weighted_list, key=operator.itemgetter(1))[0]

  played_probs = defaultdict(lambda: 1)
  opp_probs = defaultdict(lambda: defaultdict(lambda: 1))
  my_probs = defaultdict(lambda: defaultdict(lambda: 1))
  both_probs = defaultdict(lambda: defaultdict(lambda: 1))

  singleopp_opp_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singleopp_my_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singleopp_both_probs = defaultdict(lambda: defaultdict(lambda: 1))

  singlemy_opp_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singlemy_my_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singlemy_both_probs = defaultdict(lambda: defaultdict(lambda: 1))

  opp2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  my2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  both2_probs = defaultdict(lambda: defaultdict(lambda: 1))

  singleopp_opp2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singleopp_my2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singleopp_both2_probs = defaultdict(lambda: defaultdict(lambda: 1))

  singlemy_opp2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singlemy_my2_probs = defaultdict(lambda: defaultdict(lambda: 1))
  singlemy_both2_probs = defaultdict(lambda: defaultdict(lambda: 1))

  win_probs = defaultdict(lambda: 1)
  lose_probs = defaultdict(lambda: 1)
  tie_probs = defaultdict(lambda: 1)

  opp_answers = {'c': 1, 'b': 1, 'r': 1}
  my_answers = {'c': 1, 'b': 1, 'r': 1}

  opp2_answers = {'c': 1, 'b': 1, 'r': 1}
  my2_answers = {'c': 1, 'b': 1, 'r': 1}

  singleopp_opp_answers = {'c': 1, 'b': 1, 'r': 1}
  singleopp_my_answers = {'c': 1, 'b': 1, 'r': 1}

  singleopp_opp2_answers = {'c': 1, 'b': 1, 'r': 1}
  singleopp_my2_answers = {'c': 1, 'b': 1, 'r': 1}

  singlemy_opp_answers = {'c': 1, 'b': 1, 'r': 1}
  singlemy_my_answers = {'c': 1, 'b': 1, 'r': 1}

  singlemy_opp2_answers = {'c': 1, 'b': 1, 'r': 1}
  singlemy_my2_answers = {'c': 1, 'b': 1, 'r': 1}

  patterndict = defaultdict(str)
  patterndict2 = defaultdict(str)
  opppatterndict = defaultdict(str)
  opppatterndict2 = defaultdict(str)
  mypatterndict = defaultdict(str)
  mypatterndict2 = defaultdict(str)

  csu = [0] * 6 # consecutive strategy usage
  csc = []  # consecutive strategy candidates

  output = random.choice(["R", "P", "S"])
  hist = ""
  myhist = ""
  opphist = ""

  my = opp = my2 = opp2 =  ""
  singleopp_my = singleopp_opp = singleopp_my2 = singleopp_opp2 = ""
  singlemy_my = singlemy_opp = singlemy_my2 = singlemy_opp2 = ""

  sc = 0
  opp_strats = []
else:
  previous_opp_strats = opp_strats[:]
  previous_sc = sc

  sc = score[output + input]
  for i, c in enumerate(csc):
    if c == input:
      csu[i] += 1
    else:
      csu[i] = 0

  m = max(csu)
  opp_strats = [i for i, c in enumerate(csc) if csu[i] == m]

  if previous_sc == 1:
    for s1 in previous_opp_strats:
      for s2 in opp_strats:
        win_probs[chr(s1)+chr(s2)] += 1

  if previous_sc == 0:
    for s1 in previous_opp_strats:
      for s2 in opp_strats:
        tie_probs[chr(s1)+chr(s2)] += 1

  if previous_sc == -1:
    for s1 in previous_opp_strats:
      for s2 in opp_strats:
        lose_probs[chr(s1)+chr(s2)] += 1

  if my and opp:
    opp_answers[cscore[input+opp]] += 1
    my_answers[cscore[input+my]] += 1
  if my2 and opp2:
    opp2_answers[cscore[input+opp2]] += 1
    my2_answers[cscore[input+my2]] += 1

  if singleopp_my and singleopp_opp:
    singleopp_opp_answers[cscore[input+singleopp_opp]] += 1
    singleopp_my_answers[cscore[input+singleopp_my]] += 1
  if singleopp_my2 and singleopp_opp2:
    singleopp_opp2_answers[cscore[input+singleopp_opp2]] += 1
    singleopp_my2_answers[cscore[input+singleopp_my2]] += 1

  if singlemy_my and singlemy_opp:
    singlemy_opp_answers[cscore[input+singlemy_opp]] += 1
    singlemy_my_answers[cscore[input+singlemy_my]] += 1
  if singlemy_my2 and singlemy_opp2:
    singlemy_opp2_answers[cscore[input+singlemy_opp2]] += 1
    singlemy_my2_answers[cscore[input+singlemy_my2]] += 1

  for length in range(min(10, len(hist)), 0, -2):
    pattern = patterndict[hist[-length:]]
    if pattern:
      for length2 in range(min(10, len(pattern)), 0, -2):
        patterndict2[pattern[-length2:]] += output + input
    patterndict[hist[-length:]] += output + input

  # singleopp
  for length in range(min(5, len(opphist)), 0, -1):
    pattern = opppatterndict[opphist[-length:]]
    if pattern:
      for length2 in range(min(10, len(pattern)), 0, -2):
        opppatterndict2[pattern[-length2:]] += output + input
    opppatterndict[opphist[-length:]] += output + input

  # singlemy
  for length in range(min(5, len(myhist)), 0, -1):
    pattern = mypatterndict[myhist[-length:]]
    if pattern:
      for length2 in range(min(10, len(pattern)), 0, -2):
        mypatterndict2[pattern[-length2:]] += output + input
    mypatterndict[myhist[-length:]] += output + input

  played_probs[input] += 1
  opp_probs[opp][input] += 1
  my_probs[my][input] += 1
  both_probs[my+opp][input] += 1

  opp2_probs[opp2][input] += 1
  my2_probs[my2][input] += 1
  both2_probs[my2+opp2][input] += 1

  hist += output + input
  myhist += output
  opphist += input

  my = opp = my2 = opp2 = ""
  singleopp_my = singleopp_opp = singleopp_my2 = singleopp_opp2 = ""
  singlemy_my = singlemy_opp = singlemy_my2 = singlemy_opp2 = ""

  for length in range(min(10, len(hist)), 0, -2):
    pattern = patterndict[hist[-length:]]
    if pattern != "":
      my = pattern[-2]
      opp = pattern[-1]
      for length2 in range(min(10, len(pattern)), 0, -2):
        pattern2 = patterndict2[pattern[-length2:]]
        if pattern2 != "":
          my2 = pattern2[-2]
          opp2 = pattern2[-1]
          break
      break

  # singleopp
  for length in range(min(5, len(opphist)), 0, -1):
    pattern = opppatterndict[opphist[-length:]]
    if pattern != "":
      singleopp_my = pattern[-2]
      singleopp_opp = pattern[-1]
      for length2 in range(min(10, len(pattern)), 0, -2):
        pattern2 = opppatterndict2[pattern[-length2:]]
        if pattern2 != "":
          singleopp_my2 = pattern2[-2]
          singleopp_opp2 = pattern2[-1]
          break
      break

  # singlemy
  for length in range(min(5, len(myhist)), 0, -1):
    pattern = mypatterndict[myhist[-length:]]
    if pattern != "":
      singlemy_my = pattern[-2]
      singlemy_opp = pattern[-1]
      for length2 in range(min(10, len(pattern)), 0, -2):
        pattern2 = mypatterndict2[pattern[-length2:]]
        if pattern2 != "":
          singlemy_my2 = pattern2[-2]
          singlemy_opp2 = pattern2[-1]
          break
      break

  probs = {}
  for hand in rps:
    probs[hand] = played_probs[hand]

  if my and opp:
    for hand in rps:
      probs[hand] *= opp_probs[opp][hand] * my_probs[my][hand] * both_probs[my+opp][hand]
      probs[hand] *= opp_answers[cscore[hand+opp]] * my_answers[cscore[hand+my]]


    csc = [opp, beat[opp], cede[opp], my, cede[my], beat[my]]

    strats_for_hand = {'R': [], 'P': [], 'S': []}
    for i, c in enumerate(csc):
      strats_for_hand[c].append(i)

    if sc == 1:
      pr = win_probs
    if sc == 0:
      pr = tie_probs
    if sc == -1:
      pr = lose_probs

    for hand in rps:
      for s1 in opp_strats:
        for s2 in strats_for_hand[hand]:
          probs[hand] *= pr[chr(s1)+chr(s2)]
  else:
    csc = []

  if singleopp_my and singleopp_opp:
    for hand in rps:
      probs[hand] *= singleopp_opp_probs[singleopp_opp][hand] * \
                     singleopp_my_probs[singleopp_my][hand] * \
                     singleopp_both_probs[singleopp_my+singleopp_opp][hand]
      probs[hand] *= singleopp_opp_answers[cscore[hand+singleopp_opp]] * singleopp_my_answers[cscore[hand+singleopp_my]]

  if singlemy_my and singlemy_opp:
    for hand in rps:
      probs[hand] *= singlemy_opp_probs[singlemy_opp][hand] * \
                     singlemy_my_probs[singlemy_my][hand] * \
                     singlemy_both_probs[singlemy_my+singlemy_opp][hand]
      probs[hand] *= singlemy_opp_answers[cscore[hand+singlemy_opp]] * singlemy_my_answers[cscore[hand+singlemy_my]]

  if my2 and opp2:
    for hand in rps:
      probs[hand] *= opp2_probs[opp2][hand] * my2_probs[my2][hand] * both2_probs[my2+opp2][hand]
      probs[hand] *= opp2_answers[cscore[hand+opp2]] * my2_answers[cscore[hand+my2]]

  if singleopp_my2 and singleopp_opp2:
    for hand in rps:
      probs[hand] *= singleopp_opp2_probs[singleopp_opp2][hand] *\
                     singleopp_my2_probs[singleopp_my2][hand] *\
                     singleopp_both2_probs[singleopp_my2+singleopp_opp2][hand]
      probs[hand] *= singleopp_opp2_answers[cscore[hand+singleopp_opp2]] * \
                     singleopp_my2_answers[cscore[hand+singleopp_my2]]

  if singlemy_my2 and singlemy_opp2:
    for hand in rps:
      probs[hand] *= singlemy_opp2_probs[singlemy_opp2][hand] *\
                     singlemy_my2_probs[singlemy_my2][hand] *\
                     singlemy_both2_probs[singlemy_my2+singlemy_opp2][hand]
      probs[hand] *= singlemy_opp2_answers[cscore[hand+singlemy_opp2]] * \
                     singlemy_my2_answers[cscore[hand+singlemy_my2]]

  output = counter_prob(probs)
