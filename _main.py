# pylint: disable=invalid-name
import utilities
from single_cell import SingleCell
from grid import Grid
from show_grid import ShowGrid


# for example
columns = 12    # max 26
rows = 6
# density of mines  dens = mines/all cells  (higher value -> less mines)
dens = 20

# generating a random board
a_main = utilities.generate_random_string(columns, rows, dens)

# Grid
current_grid = Grid(rows, a_main)

# player input
while True:
    ShowGrid.print_board(current_grid)
    inp: str = input(
        'Enter o/f (for open/flag a cell), column letter and row number (oA3/fA3): '
    ).lower().replace(' ', '')

    inp_column = ord(
        ''.join([x for x in inp[1:] if not x.isdigit()]).upper()
    ) - 65
    inp_row = int(''.join([x for x in inp[1:] if x.isdigit()])) - 1

    if inp[0] == 'o':
        current_move = current_grid.open_cell(SingleCell(inp_column, inp_row))
        ShowGrid.print_board(current_grid)
        if current_grid.check_game_won:
            ShowGrid.print_board(current_grid, True)
            print('Congratulations! You won the game!\n')
            break
        if current_move == '9':
            ShowGrid.print_board(current_grid, True)
            print('Game over!\n')
            break
    elif inp[0] == 'f':
        current_grid.flag_cell(SingleCell(inp_column, inp_row))
