from typing import List, Union

from click import get_terminal_size


class Table:
    def __init__(self, header, rows, max_width: Union[int, None] = None):
        self.header = header
        self.rows = rows
        self.max_width = get_terminal_size()[0] if max_width is None else max_width

    def cols_sizes(self) -> List[int]:
        cols = [0]* len(self.header)
        for row in [self.header] + self.rows:
            for i, col in enumerate(row):
                cols[i] = max(cols[i], len(col))
        return cols

    def table_width(self) -> int:
        return sum(self.cols_sizes()) + ((len(self.header) - 1) * 2)

    def _get_table_row(self, row, sizes) -> str:
        return '  '.join([
            ('{:<%d}' % (sizes[i])).format(field)
            for i, field in enumerate(row)
        ])

    def table(self) -> str:
        sizes = self.cols_sizes()
        text = self._get_table_row(self.header, sizes) + '\n'
        text += self._get_table_row(['-' * size for size in sizes], sizes) + '\n'
        for row in self.rows:
            text += self._get_table_row(row, sizes)
            text += '\n'
        return text

    def description_list(self) -> str:
        field_width = max([len(field) for field in self.header])
        field_format = '{:<%d}' % (field_width)
        formatted_rows = []
        for row in self.rows:
            formatted_rows.append('\n'.join([
                '{}  {}'.format(field_format.format(self.header[i]), value)
                for i, value in enumerate(row)
            ]))
        return '\n\n'.join(formatted_rows)

    def get_by_max_with(self) -> str:
        if self.table_width() <= self.max_width:
            return self.table()
        else:
            return self.description_list()

    def __str__(self):
        return self.get_by_max_with()
