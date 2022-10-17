# Tic-Tac-Toe-with-AI
## Preview


https://user-images.githubusercontent.com/67506662/196250519-c23c1f34-df92-4bd3-8364-22f17f3126ff.mp4


## Description
- An interactive tic tac toe using AI.<br>
- The game can be played with one of two modes
  - human vs AI
  - AI vs AI
- AI difficulties
  - ***easy*** : The AI makes random moves.
  - ***medium***: The AI try one of these three logics
  1. if the it has two in a row and can win with one further move then make move.
  2. if the opponent can win with one move, it plays the move necessary to block this win.
  3. play random move.
  - ***hard*** : the AI use [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm.

## How to play
- Run the game 
``` shell 
 python3 tictactoe.py
```
- To start the game use the following command<br> 
 `start <user|easy|medium|hard> <user|easy|medium|hard>`<br>
- `<user|easy|medium|hard>` represent the player.<br>
- `user` human player.<br>
- `<easy|medium|hard>` AI.<br>
- To end the game use the following command<br>`exit`
