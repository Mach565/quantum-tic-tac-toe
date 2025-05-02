# README

## Introduction

This is an implementation of [quantum tic-tac-toe](https://en.wikipedia.org/wiki/Quantum_tic-tac-toe), written in Python for the terminal. The version of Python used to create this was Python 3.12, later or eariler versions may work, but aren't guaranteed to do so.

Currently, the game requires two players to play. Singleplayer versus AI may come at a later date.

## Playing

Just run `python quantum-tic-tac-toe.py` and start playing

Each turn, a player places two marks on the board. These marks are *spooky marks*, have a subscript indicating what turn they were played on (starting from 1) and are not counted in scoring. The two spaces that are marked are said to be *entangled*.

Once a cyclic entanglement is formed, that is, there is a series of entanglements that when followed, return to the same square, the player who did not create the cyclic entanglement is asked to measure it. Once measured, the spooky marks collapse into *classical marks*, which do count for scoring and do not allow for any further spooky marks to be played in their space. A player wins once they have three classical marks in a row, column, or diagonal.

Due to the way measurements are performed, it is possible for both players to gain a three classical marks in a row or column at the same time. In that case, the player with the lower maximum subscript is the winner and gets a full point, whereas the player with the higher maximum subscript gets only half a point.
