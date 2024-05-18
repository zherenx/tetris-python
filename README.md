# TETRIS

Tetris game using Python and the pygame modules

<img src="res/game_screen.png" alt="game_screen" width="500">

## Control

This game follows the standard Tetris controls, use Left or Right key to shift the current tetromino horizontally, use Up key to rotate the current tetromino clockwise by 90 degrees, and use Down key to speed up the down fall

At anytime, player can press 'R' key on keyboard to restart the game, or press 'Esc' key to exit the game

## Scoring and Leveling

The Scoring system I used in this version took inspiration from different [scoring systems](https://tetris.wiki/Scoring), and it was designed in a way which encouranges players to clear multiple lines at once.

As for now, clearing 1, 2, 3, 4 lines will grant player 40, 100, 300, 1200 base points before any multipliers. Your final score earned per clearance would be equal to (base points * multiplier).

There are two multipliers, the level multiplier and Tetris multiplier. The level multiplier is equal to the current level; the game starts at level 1, and player will level up every time it clears 8 lines or more (counter reset when level up; currently max level is set to 10), and free fall speed will increase by 25 percents compare to the previous level. The Tetris multiplier is activated through previous Tetris clearance (clear 4 lines at once), and it will double the score earned for the next clearance when activated.
