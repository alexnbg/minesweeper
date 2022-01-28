import random


def generate_random_string(columns: int, rows: int, density: int):
    """Generates and returns a string of 'T' and 'F'
    with random placed mines and lenght = columns*rows.
      columns/rows (int) : the size of the grid and the string
      density (int) : the number of empty cells per single mine (higher value -> less mines)"""

    mines = int(columns*rows/density) + (columns*rows % density > 0)
    out_list = ['F']*columns*rows

    while out_list.count('T') < mines:
        ind = random.randint(0, columns*rows-1)
        if out_list[ind] == 'F':
            out_list[ind] = 'T'

    return ''.join(out_list)


def conv_str_to_list(tf_string: str) -> list:
    """Converts a string of 'T' and 'F' into a list of True and False."""
    out_list = []
    for cell in tf_string:
        if cell == 'T':
            out_list.append(True)
        elif cell == 'F':
            out_list.append(False)
    return out_list


def conv_list_to_str(tf_list: list) -> str:
    """Converts a list of True and False into a string of 'T' and 'F'."""
    out_list = []
    for cell in tf_list:
        if cell:
            out_list.append('T')
        else:
            out_list.append('F')
    return ''.join(out_list)
