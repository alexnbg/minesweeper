import utilities
from single_cell import SingleCell


class Grid:
    """Creates and manages a game.\n
    For a new game is needed:
      columns (int): number of columns
      game_string_tf (str): string of 'T' and 'F' for cells with or without mines\n
    For continue an old game is also needed:
      opened_string_tf (str): string of 'T' and 'F' for opened and closed cells
      flagged_string_tf (str): string of 'T' and 'F' for flagged and unflagged cells"""

    def __init__(
            self,
            columns: int,
            game_string_tf: str,
            opened_string_tf: str = None,
            flagged_string_tf: str = None) -> None:

        # Parameters of the grid
        self.columns = columns
        self.rows = int(len(game_string_tf)/columns)
        self.mines = game_string_tf.count('T')

        # Strings remembering cells values
        self.main_str = game_string_tf
        """String of 'T' and 'F' for cells with or without mines ."""
        self.calculated_str = self._calculate_string(
            self.columns,
            game_string_tf)
        """String of digits representing every cell value as\n
        cells with mines (9) / cells with nearby mines (1-8) / cells without nearby mines (0)."""

        # Lists to keep track of opened and flagged cells
        self.opened_list = [
            False] * len(game_string_tf) if not opened_string_tf else utilities.conv_str_to_list(
                opened_string_tf)
        """List of True and False to track opened and closed cells."""
        self.flagged_list = [
            False] * len(game_string_tf) if not flagged_string_tf else utilities.conv_str_to_list(
                flagged_string_tf)
        """List of True and False to track cells with flags and without."""

    @staticmethod
    def _calculate_string(columns: int, game_string_tf: str) -> str:
        """Takes a string of 'F' and 'T' ('T' for mine, 'F' for empty)
        and returns a string of numbers (for a grid with a given number of columns).\n
        9   : a cell containing a mine
        1-8 : an empty cell showing the number of nearby mines touching this cell
        0   : an empty cell, that don't touch any nearby mines"""

        rows = int(len(game_string_tf)/columns)
        out_list = list(game_string_tf)

        for ind, let in enumerate(game_string_tf):
            if let == 'F':
                column = ind % columns
                row = ind // columns
                set_cells = Grid._get_neighboring_cells(
                    SingleCell(column, row),
                    columns,
                    rows)

                count_mines = 0
                for cell_ind in set_cells:
                    if game_string_tf[cell_ind] == 'T':
                        count_mines += 1

                out_list[ind] = str(count_mines)
            elif let == 'T':
                out_list[ind] = '9'

        return ''.join(out_list)

    @staticmethod
    def _get_single_cell(long_index: int, columns: int) -> SingleCell:
        """Returns a SingleCell object for a given index (for a sequence of True/False) and a grid columns."""
        return SingleCell(long_index % columns, long_index//columns)

    @staticmethod
    def _get_neighboring_cells(cell: SingleCell, columns: int, rows: int) -> set:
        """Returns a set containing the indexes (for a sequence of True/False)
        of all neighboring cells of a given SingleCell object.
        Within a grid of given columns and rows."""

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

    def _get_unflagged_neighboring_cells(self, cell: SingleCell) -> set:
        """Returns a set containing the indexes (for a sequence of True/False)
        of all unflagged neighboring cells of a given SingleCell object, for the current Grid."""
        set_cells = set()
        for ind in self._get_neighboring_cells(cell, self.columns, self.rows):
            if not self.flagged_list[ind]:
                set_cells.add(ind)
        return set_cells

    def _get_connected_cells(self, cell: SingleCell) -> set:
        """Returns a set containing the indexes (for a sequence of True/False)
        of all unflagged neighboring cells to a given empty cell
        and their unflagged neighboring cells for any empty cell and so on."""

        set_cells: set = self._get_unflagged_neighboring_cells(cell)

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
                        self._get_unflagged_neighboring_cells(
                            self._get_single_cell(c_ind, self.columns))
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
        """Mark an unopened cell as flagged or remove flag if the cell is already flagged."""
        ind = cell.long_index(self.columns)
        if not self.opened_list[ind]:
            self.flagged_list[ind] = not self.flagged_list[ind]

    def open_cell(self, cell: SingleCell) -> str:
        """Open an unopened and unflagged cell and returns cell's value or 'flagged'."""

        ind = cell.long_index(self.columns)

        if not self.flagged_list[ind]:
            cell_number = int(self.calculated_str[ind])

            if cell_number == 0:
                connected: set = self._get_connected_cells(cell)
                for c_ind in connected:
                    self.opened_list[c_ind] = True
            # maybe check for other values and do something

            self.opened_list[ind] = True
            return str(cell_number)

        return 'flagged'

    @property
    def check_game_won(self) -> bool:
        """Returns True/False if all cells, that don't contain mines, are revealed."""
        for ind, let in enumerate(self.main_str):
            if let == 'F' and not self.opened_list[ind]:
                return False
        return True

    @property
    def opened_string(self) -> str:
        """Return a string of 'T' and 'F' representing opened and closed cells."""
        return utilities.conv_list_to_str(self.opened_list)

    @property
    def flagged_string(self) -> str:
        """Return a string of 'T' and 'F' representing flagged and unflagged cells."""
        return utilities.conv_list_to_str(self.flagged_list)
