import random


def generate_random_string(columns: int, rows: int, density: int):
    """Generates and returns a string of 'T' and 'F'\n
    with random placed mines and lenght = columns*rows.\n
    columns/rows - the size of the grid and the string\n
    density - the number of empty cells per single mine (higher value -> less mines)"""

    mines = int(columns*rows/density) + (columns*rows % density > 0)
    out_list = ['F']*columns*rows

    while out_list.count('T') < mines:
        ind = random.randint(0, columns*rows-1)
        if out_list[ind] == 'F':
            out_list[ind] = 'T'

    return ''.join(out_list)
