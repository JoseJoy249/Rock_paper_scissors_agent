This repository contains the code to build an agent to play rock paper scissors. The agent uses Lempel Ziv and Context tree 
weighting models to estimate the underlying probability distribution from the opponents move, to deliver the counter move.

Since the model needs few examples to train itself, the first few moves would be a combination of predicted moves with some 
randomness injected. The amount of randomness decreases as more moves are played by the opponent.

