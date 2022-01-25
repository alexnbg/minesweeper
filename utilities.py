import random


def generate_random_string(columns: int, rows: int, density: int):
    mines = int(columns*rows/density) + (columns*rows % density > 0)
    out_str = 'F'*columns*rows

    while out_str.count('T') < mines:
        ind = random.randint(0, columns*rows-1)
        if out_str[ind] == 'F':
            out_str = out_str[:ind]+'T'+out_str[ind+1:]

    return out_str


def calculate_string(rows: int, bstr: str):
    columns = int(len(bstr)/rows)
    out_str = bstr.replace('T', '9')

    for ind in range(len(out_str)):
        if out_str[ind] == 'F':
            column = ind % rows
            row = ind // columns
            count_m = 0

            if row != 0:
                if column == 0:
                    count_m += out_str[(row-1)*columns+(column):
                                       (row-1)*columns+(column+1)+1].count('9')
                elif column < columns-1:
                    count_m += out_str[(row-1)*columns+(column-1):
                                       (row-1)*columns+(column+1)+1].count('9')
                elif column == columns-1:
                    count_m += out_str[(row-1)*columns+(column-1):
                                       (row-1)*columns+(column)+1].count('9')

            if column == 0:
                count_m += out_str[row*columns + (column):
                                   row*columns+(column+1)+1].count('9')
            elif column < columns-1:
                count_m += out_str[row*columns + (column-1):
                                   row*columns+(column+1)+1].count('9')
            elif column == columns-1:
                count_m += out_str[row*columns + (column-1):
                                   row*columns+(column)+1].count('9')

            if row != rows-1:
                if column == 0:
                    count_m += out_str[(row+1)*columns+(column):
                                       (row+1)*columns+(column+1)+1].count('9')
                elif column < columns-1:
                    count_m += out_str[(row+1)*columns+(column-1):
                                       (row+1)*columns+(column+1)+1].count('9')
                elif column == columns-1:
                    count_m += out_str[(row+1)*columns+(column-1):
                                       (row+1)*columns+(column)+1].count('9')

            out_str = out_str[:ind]+str(count_m)+out_str[ind+1:]

    return out_str
