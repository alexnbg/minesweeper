from grid import Grid


class ShowGrid:

    closed = '_'
    flagged = 'f'
    empty = ' '
    mine = '*'

    @classmethod
    def print_board(cls, grid: Grid, show_mines: bool = False):

        # grid string to be printed
        gr_str = cls._get_print_string(grid, show_mines)

        # spacing - columns width and between columns
        header_rows = 3
        header_column = 1
        if grid.rows > 99:
            header_rows = 4
        if grid.columns > 26:
            header_column = 2
        elif grid.columns > 52:
            header_column = 3

        #
        # Print board
        #

        print()
        # print header for columns (A, B, C, ...)
        print(
            ' '*header_rows,
            ' '.join(
                [f'{chr(65+column)}'.center(header_column)
                 for column in range(grid.columns)]
            )
        )
        # print rows and cells (row number + cells...)
        for row in range(grid.rows):
            print(
                # number of row
                str(row+1).rjust(header_rows),
                # cells - opened/closed/flagged
                ' '.join(list(str(
                    gr_str[row * grid.columns:(row+1) * grid.columns]
                ).center(header_column)))
            )
        print()

    @classmethod
    def _get_print_string(cls, grid: Grid, show_mines: bool = False) -> str:
        out_list = []
        for ind, cell in enumerate(grid.opened_string):
            if cell == 'F':
                if show_mines and grid.main_str[ind] == 'T':
                    out_list.append(cls.mine)
                elif grid.flagged_string[ind] == 'T':
                    out_list.append(cls.flagged)
                else:
                    out_list.append(cls.closed)
            else:
                num_str = grid.calculated_str[ind]
                if int(num_str) == 0:
                    out_list.append(cls.empty)
                elif int(num_str) == 9:
                    out_list.append(cls.mine)
                else:
                    out_list.append(num_str)

        return ''.join(out_list)
