### Go-Moku MCTS Agent by Jort de Boer

This folder represents my Gomoku-Agent based on the Monte Carlo Tree Search algorithm.

## Files

Frist we need the 'gmPlayer_AI.py'. This is the file where the 'standard' MOVE function is located.
You also need the 'mcts_utils.py' and the 'gmAIgent.py'.

The 'mcts_utils.py' is the file where the mcts algorithm is defined. All the functions and utilities are in there.
The 'gmAIgent.py' contains the functionality for my smart AI.

## Functionalities of my AI

My agent has a very efficient way of finding the best possible moves on a particulair state.

We look for so called 'sequences'. This means, stones with the same color in a row. We can check the sequences for all the stones on the board and based on the length of the sequence we act.
The AI is primarily set to prioritize defence, but could be changed to offense if we change the 'self.pref_atack' in the 'gm_Player_AI.py'.

We get these sequences based on a pre-defined Matrix. We check all the directions and sum the amount of stones of a color in a row. 

This image illustrates the way the matrix is created:
![all text](https://github.com/Jordieboyz/ALDS_2022/blob/a1ee0cb8ab3200880590529ce5415f6f8d5752a9/Gomoku%20Eindopdracht/MatrixExplanation.png)

## should/must-haves

I obviously implemented the mcts-algorithm as for the name in the id-function in 'gm_Player_AI.py' 
There are also comment which explain the Big-Oh for almost all the functions.

I do have a couple opening moves. These moves are called 'star points'. 
The function of this opening is to create some sort of territory and places to start sequences of and if we move in the right direction, we just have to place 3 stones to win (if we are black)
Territory is important in a game like this, becuase is doesn't seem to matter in the start of the game, but later is is very annoying if we can only defend and not presure the opponent by attacking ourself.

I did change the exploration method. originally it was simply too much to compute in the given time to get a good result out of the rollout. There we're just too less rollout. Defenitely in the early game.
So I decreased the amount of possible moves by a significatn amount. This results in more accurate rollouts. 

I also tried changing the constant C valus for the uct-formula. Unfortunately, the way i created my AI, there is nog much of a difference so I took it out of the final product.

I tested everything quite a bit, so it should all wrk fine :)
