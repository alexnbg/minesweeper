from dataclasses import dataclass


@dataclass
class SingleCell:
    column: int
    row: int

    def long_index(self, columns) -> int:
        return self.row*columns + self.column
