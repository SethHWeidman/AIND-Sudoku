# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

The program that actually solves the Sudoku is the `solution.py` file.

The file implements the simple, self-explanatory `eliminate` and `only_choice` strategies, as well as more advance `naked_twins` strategy, which is well-commented if you want to see how I did it.

The `search` function does depth-first search, and the `solve` function does runs the other functions until the Sudoku is solved.
