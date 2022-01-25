# pylint: disable=missing-module-docstring, invalid-name

import utilities
from single_cell import SingleCell
from grid import Grid
from show_grid import ShowGrid


# Game parameters
columns = 12    # max 26
rows = 6
# density of mines  dens = mines/all cells  (higher value -> less mines)
density = 7

# 1
# generating a string with random mines
a_main = utilities.generate_random_string(columns, rows, density)

# 2
# create a Grid object with the generated string
current_grid = Grid(columns, a_main)

# 3
# player input
# loop until the game is over or an error occur
while True:
    # print the game
    ShowGrid.print_board(current_grid)

    # input from the player
    input_str: str = input(
        'Enter o/f (for open/flag a cell), column letter and row number (oA3/fA3): '
    ).lower().replace(' ', '')

    # take index of column and row from the input and create a SingleCell object
    input_column = ord(
        ''.join([x for x in input_str[1:] if not x.isdigit()]).upper()
    ) - 65
    input_row = int(''.join([x for x in input_str[1:] if x.isdigit()])) - 1
    # create a SingleCell object with the location of the choosed cell
    input_cell = SingleCell(input_column, input_row)

    # check and execute the action from the input
    # open or flag
    if input_str[0] == 'o':
        # get response from the Grid object when opening the cell
        open_cell_response = current_grid.open_cell(input_cell)

        # check if all cells without mines are already opened - game won
        if current_grid.check_game_won:
            ShowGrid.print_board(current_grid, True)
            print('Congratulations! You won the game!\n')
            break

        # if the cell has a mine - game lost
        if open_cell_response == '9':
            ShowGrid.print_board(current_grid, True)
            print('Game over!')
            print('You lost!')
            print()
            break
    elif input_str[0] == 'f':
        current_grid.flag_cell(input_cell)
