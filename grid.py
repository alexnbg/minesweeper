from single_cell import SingleCell


class Grid:
    def __init__(
            self,
            columns: int,
            board_string_TF: str,
            opened_string_TF: str = None,
            flagged_string_TF: str = None) -> None:

        # Parameters of the grid
        self.columns = columns
        self.rows = int(len(board_string_TF)/columns)
        self.mines = board_string_TF.count('T')

        # String of T and F for cels with a mine or without a mine
        self.main_str = board_string_TF
        # String with numbers representing cells with mines/empty/nearby mines
        self.calculated_str = self._calculate_string(
            self.columns,
            board_string_TF)

        # Lists to keep track of opened and flagged cells
        self.opened_list = [
            'F'] * len(board_string_TF) if not opened_string_TF else list(opened_string_TF)
        self.flagged_list = [
            'F'] * len(board_string_TF) if not flagged_string_TF else list(opened_string_TF)

    @staticmethod
    def _calculate_string(columns: int, board_string_TF: str) -> str:
        """Takes a string of 'F' and 'T' ('T' for mine, 'F' for empty)\n
        and returns a string of numbers (for a grid with a given number of columns).\n
        9   - a cell containing a mine\n
        1-8 - an empty cell showing the number of nearby mines touching this cell\n
        0   - an empty cell, that don't touch any mines"""

        rows = int(len(board_string_TF)/columns)
        out_list = list(board_string_TF)

        for ind, let in enumerate(board_string_TF):
            if let == 'F':
                column = ind % columns
                row = ind // columns
                set_cells = Grid._get_neighboring_cells(
                    SingleCell(column, row),
                    columns,
                    rows)

                count_mines = 0
                for cell_ind in set_cells:
                    if board_string_TF[cell_ind] == 'T':
                        count_mines += 1

                out_list[ind] = str(count_mines)
            elif let == 'T':
                out_list[ind] = '9'

        return ''.join(out_list)

    @staticmethod
    def _get_single_cell(long_index: int, columns: int) -> SingleCell:
        """Returns a SingleCell object for a given long index and columns."""
        return SingleCell(long_index % columns, long_index//columns)

    @staticmethod
    def _get_neighboring_cells(cell: SingleCell, columns: int, rows: int) -> set:
        """Returns a set containing the long indexes (integers) \n
        of all neighboring cells of a given SingleCell object.\n
        Within a grid of given columns x rows."""

        set_cells = set()

        # checks if the cell is first/last of the column/row
        cell_col_0 = -1
        cell_col_1 = 1
        if cell.column == 0:
            cell_col_0 = 0
        elif cell.column == columns-1:
            cell_col_1 = 0

        cell_row_0 = -1
        cell_row_1 = 1
        if cell.row == 0:
            cell_row_0 = 0
        elif cell.row == rows - 1:
            cell_row_1 = 0

        # add the long indexes of all 8 neighboring cells
        set_cells.add(SingleCell(
            cell.column+cell_col_0, cell.row+cell_row_0).long_index(columns))
        set_cells.add(SingleCell(
            cell.column, cell.row+cell_row_0).long_index(columns))
        set_cells.add(SingleCell(
            cell.column+cell_col_1, cell.row+cell_row_0).long_index(columns))
        set_cells.add(SingleCell(
            cell.column+cell_col_0, cell.row).long_index(columns))
        set_cells.add(SingleCell(
            cell.column+cell_col_1, cell.row).long_index(columns))
        set_cells.add(SingleCell(
            cell.column+cell_col_0, cell.row+cell_row_1).long_index(columns))
        set_cells.add(SingleCell(
            cell.column, cell.row+cell_row_1).long_index(columns))
        set_cells.add(SingleCell(
            cell.column+cell_col_1, cell.row+cell_row_1).long_index(columns))

        return set_cells

    def _get_connected_cells(self, cell: SingleCell) -> set:
        """Returns a set containing the long indexes (integers) \n
        of all neighboring cells to a given empty cell\n
        and their neighboring cells for any empty cell and so on."""

        set_cells: set = self._get_neighboring_cells(
            cell, self.columns, self.rows)

        # keep tracks of the number of any empty cell (without nearby mines)
        empty_cells_0 = 0
        empty_cells = 0
        for ind in set_cells:
            if int(self.calculated_str[ind]) == 0:
                empty_cells += 1

        # loops until the neigboring cells of all connected empty cells are added to the set
        while empty_cells > empty_cells_0:
            empty_cells_0 = empty_cells
            new_set = set()
            for c_ind in set_cells:
                if int(self.calculated_str[c_ind]) == 0:
                    new_set.update(
                        self._get_neighboring_cells(
                            self._get_single_cell(c_ind, self.columns),
                            self.columns,
                            self.rows)
                    )
            set_cells.update(new_set)
            empty_cells = 0
            for s_ind in set_cells:
                if int(self.calculated_str[s_ind]) == 0:
                    empty_cells += 1

        # removes the given cell if it is in the set
        if cell.long_index(self.columns) in set_cells:
            set_cells.remove(cell.long_index(self.columns))

        return set_cells

    def flag_cell(self, cell: SingleCell) -> None:
        """Mark an unopened cell as flagged."""
        self.flagged_list[cell.long_index(self.columns)] = 'T'

    def open_cell(self, cell: SingleCell) -> str:
        """Open an unopened and unflagged cell and returns cell's number or 'flagged'."""

        ind = cell.long_index(self.columns)

        if self.flagged_list[ind] == 'F':
            cell_number = int(self.calculated_str[ind])

            if cell_number == 0:
                connected: set = self._get_connected_cells(cell)
                for c_ind in connected:
                    self.opened_list[c_ind] = 'T'
            # maybe check for other values and take some actions - in the future

            self.opened_list[ind] = 'T'
            return str(cell_number)

        return 'flagged'

    @property
    def check_game_won(self) -> bool:
        """Returns True/False if all cells, that don't contain mines, are revealed."""

        for ind, let in enumerate(self.main_str):
            if let == 'F' and self.opened_list[ind] != 'T':
                return False
        return True

    @property
    def opened_string(self) -> str:
        """Return a string of 'T' and 'F' representing opened and unopened cells."""
        return ''.join(self.opened_list)

    @property
    def flagged_string(self) -> str:
        """Return a string of 'T' and 'F' representing flagged and unflagged cells."""
        return ''.join(self.flagged_list)
