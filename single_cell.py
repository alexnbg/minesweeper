from dataclasses import dataclass


@dataclass
class SingleCell:
    """Class for storing the location (column, row) of a cell."""

    column: int
    row: int

    def long_index(self, columns) -> int:
        """Returns the index (for a sequence of True/False) of a given cell with location
        for a grid of a given number of columns."""
        return self.row*columns + self.column
