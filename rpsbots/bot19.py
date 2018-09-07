#Iocaine powder based AI

import random

# 2 different lengths of history, 3 kinds of history, both, mine, yours
# 6 kinds of strategy based on Iocaine Powder
num_predictor = 36

if input=="":
    len_rfind = [20,6]
    beat = { "R":"P" , "P":"S", "S":"R"}
    not_lose = { "R":"PR" , "P":"SP" , "S":"RS" } #50-50 chance
    my_his   =""
    your_his =""
    both_his =""
    list_predictor = [""]*num_predictor
    length = 0
    temp1 = { "PP":"1" , "PR":"2" , "PS":"3",
              "RP":"4" , "RR":"5", "RS":"6",
              "SP":"7" , "SR":"8", "SS":"9"}
    score_predictor = [0]*num_predictor
    output = random.choice("RPS")
    predictors = [output]*num_predictor
else:
    #update predictors

    if len(list_predictor[0])<5:
        front =0
    else:
        front =1
    for i in range (num_predictor):
        if predictors[i]==input:
            result ="1"
        else:
            result ="0"
        list_predictor[i] = list_predictor[i][front:5]+result #only 5 rounds before
    """
    if length == 30 or length==29:
        print score_predictor.index(max(score_predictor))
        print front
        for i in range (num_predictor):
            print i, list_predictor[i], predictors[i]
    """
    """
    for i in range(num_predictor):
        score_predictor[i]*= 0.8
        if input==predictors[i]:
            score_predictor[i] +=3
        else:
            score_predictor[i] -=3
    """
    #history matching 1-12
    my_his += output
    your_his += input
    both_his += temp1[input+output]
    length +=1
    for i in range(2):
        len_size = min(length,len_rfind[i])
        j=len_size
        #both_his
        while j>=1 and not both_his[length-j:length] in both_his[0:length-1]:
            j-=1
        if j>=1:
            k = both_his.rfind(both_his[length-j:length],0,length-1)
            predictors[0+6*i] = your_his[j+k]
            predictors[1+6*i] = beat[my_his[j+k]]
        else:
            predictors[0+6*i] = random.choice("RPS")
            predictors[1+6*i] = random.choice("RPS")
        j=len_size
        #your_his
        while j>=1 and not your_his[length-j:length] in your_his[0:length-1]:
            j-=1
        if j>=1:
            k = your_his.rfind(your_his[length-j:length],0,length-1)
            predictors[2+6*i] = your_his[j+k]
            predictors[3+6*i] = beat[my_his[j+k]]
        else:
            predictors[2+6*i] = random.choice("RPS")
            predictors[3+6*i] = random.choice("RPS")
        j=len_size
        #my_his
        while j>=1 and not my_his[length-j:length] in my_his[0:length-1]:
            j-=1
        if j>=1:
            k = my_his.rfind(my_his[length-j:length],0,length-1)
            predictors[4+6*i] = your_his[j+k]
            predictors[5+6*i] = beat[my_his[j+k]]
        else:
            predictors[4+6*i] = random.choice("RPS")
            predictors[5+6*i] = random.choice("RPS")

    #rotate 13-36:
    for i in range(12,36):
        predictors[i] = beat[beat[predictors[i-12]]]

    #choose a predictor
    len_his = len(list_predictor[0])
    for i in range(num_predictor):
        sum = 0
        for j in range(len_his):
            if list_predictor[i][j]=="1":
                sum+=(j+1)*(j+1)
            else:
                sum-=(j+1)*(j+1)
        score_predictor[i] = sum
    max_score = max(score_predictor)
    min_score = min(score_predictor)
    #print max_score
    output = beat[predictors[score_predictor.index(max_score)]]
    """
    predict = predictors[score_predictor.index(max(score_predictor))]
    output = beat[predict]
    #output = random.choice(not_lose[predict])
    """
