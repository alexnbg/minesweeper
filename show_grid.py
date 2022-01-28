from grid import Grid


class ShowGrid:
    """Class for only printing a Grid object."""

    # how to print the different cells
    closed = '_'
    flagged = 'f'
    empty = ' '
    mine = '*'

    @staticmethod
    def print_board(grid: Grid, show_mines: bool = False):
        """Prints a grid of cells in columns and rows
        with the current state for every cell (closed/opened/flagged)
        for a given Grid object.\n
        If show_mines is True the game has ended and it prints where all mines are."""

        # get a string with the current state of all cells to be printed
        gr_str = ShowGrid._get_print_string(grid, show_mines)

        # spacing - columns width and between columns
        header_rows = 3
        header_column = 1
        if grid.rows > 99:
            header_rows = 4
        if grid.columns > 26:
            header_column = 2
        elif grid.columns > 52:
            header_column = 3

        # Print the grid of cells

        print()
        # print header for columns (A, B, C, ...)
        print(
            ' '*header_rows,
            ' '.join(
                [f'{chr(65+column)}'.center(header_column)
                 for column in range(grid.columns)])
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

    @staticmethod
    def _get_print_string(grid: Grid, show_mines: bool = False) -> str:
        """Return a string of the state of every cell (closed/opened/flagged).
        If show_mines is True returns the same string with revealed mines positions."""

        out_list = []

        for ind, cell in enumerate(grid.opened_string):
            if cell == 'F':
                if show_mines and grid.main_str[ind] == 'T':
                    out_list.append(ShowGrid.mine)
                elif grid.flagged_string[ind] == 'T':
                    out_list.append(ShowGrid.flagged)
                else:
                    out_list.append(ShowGrid.closed)
            else:
                num_str = grid.calculated_str[ind]
                if int(num_str) == 0:
                    out_list.append(ShowGrid.empty)
                elif int(num_str) == 9:
                    out_list.append(ShowGrid.mine)
                else:
                    out_list.append(num_str)

        return ''.join(out_list)
