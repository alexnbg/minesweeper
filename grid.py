from single_cell import SingleCell


class Grid:
    def __init__(
            self,
            rows: int,
            board_string_TF: str,
            opened_string_TF: str = None,
            flagged_string_TF: str = None) -> None:
        self.columns = int(len(board_string_TF)/rows)
        self.rows = rows
        self.mines = board_string_TF.count('T')

        self.main_str = board_string_TF
        self.calculated_str = self._calculate_string(
            self.columns, board_string_TF)

        self.opened = 'F' * len(board_string_TF) \
            if not opened_string_TF else opened_string_TF

        self.flagged = 'F' * len(board_string_TF) \
            if not flagged_string_TF else flagged_string_TF

        self.opened_list = [
            'F'] * len(board_string_TF) if not opened_string_TF else [x for x in opened_string_TF]
        self.flagged_list = [
            'F'] * len(board_string_TF) if not flagged_string_TF else [x for x in flagged_string_TF]

    @staticmethod
    def _calculate_string(columns: int, board_string_TF: str):
        rows = int(len(board_string_TF)/columns)
        # out_str = board_string_TF.replace('T', '9')
        # out_list = [x for x in board_string_TF.replace('T', '9')]
        out_list = list(board_string_TF)

        # for ind in range(len(out_str)):
        #     if out_str[ind] == 'F':
        #         column = ind % columns
        #         row = ind // columns
        #         count_mines = 0

        #         if row != 0:
        #             if column == 0:
        #                 count_mines += out_str[(row-1)*columns+(column):(row-1)*columns+(column+1)+1].count('9')
        #             elif column < columns-1:
        #                 count_mines += out_str[(row-1)*columns+(column-1):(row-1)*columns+(column+1)+1].count('9')
        #             elif column == columns-1:
        #                 count_mines += out_str[(row-1)*columns+(column-1):(row-1)*columns+(column)+1].count('9')

        #         if column == 0:
        #             count_mines += out_str[row*columns + (column):
        #                                row*columns+(column+1)+1].count('9')
        #         elif column < columns-1:
        #             count_mines += out_str[row*columns + (column-1):
        #                                row*columns+(column+1)+1].count('9')
        #         elif column == columns-1:
        #             count_mines += out_str[row*columns + (column-1):
        #                                row*columns+(column)+1].count('9')

        #         if row != rows-1:
        #             if column == 0:
        #                 count_mines += out_str[(row+1)*columns+(column):(row+1)*columns+(column+1)+1].count('9')
        #             elif column < columns-1:
        #                 count_mines += out_str[(row+1)*columns+(column-1):(row+1)*columns+(column+1)+1].count('9')
        #             elif column == columns-1:
        #                 count_mines += out_str[(row+1)*columns+(column-1):(row+1)*columns+(column)+1].count('9')

        #         out_str = out_str[:ind]+str(count_mines)+out_str[ind+1:]

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

        # return out_str
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

        # add all 8 neighboring cells to the set
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

        empty_cells_0 = 0
        empty_cells = 0

        for ind in set_cells:
            if int(self.calculated_str[ind]) == 0:
                empty_cells += 1

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

        if cell.long_index(self.columns) in set_cells:
            set_cells.remove(cell.long_index(self.columns))

        return set_cells

    def flag_cell(self, cell: SingleCell) -> None:
        """Mark an unopened cell as flagged."""
        ind = cell.long_index(self.columns)
        # self.flagged = self.flagged[:ind] + 'T' + self.flagged[ind+1:]
        self.flagged_list[ind] = 'T'

    def open_cell(self, cell: SingleCell) -> str:
        """Open an unopened and unflagged cell."""
        ind = cell.long_index(self.columns)

        # if self.flagged[ind] == 'F':
        if self.flagged_list[ind] == 'F':
            cell_number = int(self.calculated_str[ind])
            if cell_number == 0:
                connected: set = self._get_connected_cells(cell)
                for c_ind in connected:
                    # self.opened = self.opened[:c_ind] + \
                    #     'T' + self.opened[c_ind+1:]
                    self.opened_list[c_ind] = 'T'
                self.opened_list[ind] = 'T'
            elif cell_number > 0 and cell_number < 9:
                # self.opened = self.opened[:ind] + 'T' + self.opened[ind+1:]
                self.opened_list[ind] = 'T'
            elif cell_number == 9:
                self.opened_list[ind] = 'T'
                # also some other things

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
        return ''.join(self.opened_list)

    @property
    def flagged_string(self) -> str:
        return ''.join(self.flagged_list)
