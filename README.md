# minesweeper_solver
This script can solve most of the minesweeper puzzles. To launch the script you will need to install this modules: cv2, numpy, PIL and pyautogui.

You can use this website for testing - [Minesweeper](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mines.html).

1. Set variables correctly. n - number of rows, m - number of columns, k - number of bombs. They are located on lines 11-13.
2. Run the script and switch to the browser within 1 second.
```
python minesweeper.py
```
This script uses 2 strategies for solving: easy() and hard().

easy() - Marks obvious and unambiguous cells. For example cell has 2 neighbors and 2 bombs, it is obvious that all 2 neighbors are bombs.
hard() - Bruteforces all pairs of neighboring cells and uses formulas to solve the puzzle.

For example first cell has `b1` neighboring bombs and second cell has `b2` bombs.

`a1` is the number of unknown cells neighboring to first cell and `a2` is for second cell.

`y` is the number of unknown cells in the intersection of first cell and second.

`x = a1 - y` is the number of unknown cells neighboring to first cell excluding the intersection.

`z = a2 - y` is the number of unknown cells neighboring to second cell excluding the intersection.

Without loss of generality assume that `x` >= `z`.

If `b1 - min(b2, y)` equals `x` then all `x` cells are bombs.

If `b1 - x` equals `b2` then all `z` cells are safe.
