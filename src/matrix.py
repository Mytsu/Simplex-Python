"""Matrix class."""

from copy import deepcopy
from functools import partial
from itertools import chain, islice
from numbers import Number
from operator import add, mul, sub
from typing import Callable, Generator, List


class Matrix:
    """Matrix implementation with several operations available."""
    def __init__(self, rows=None, cols=None, data=None, byrow=False):
        """Matrix constructor. Examples:

        Matrix(2, 3):
            0  0  0
            0  0  0

        Matrix(3, 2, [1, 2, 3, 4, 5, 6]):
            1  4
            2  5
            3  6

        Matrix(3, 2, [1, 2, 3, 4, 5, 6], byrow=True)
            1  2
            3  4
            5  6

        Matrix(data=[[1, 3], [5, 7]]):
            1  5
            3  7

        Matrix(data=[[1, 2, 3], [11, 12, 13]], byrow=True)
             1   2   3
            11  12  13
        """
        if data is None:
            self._data = [[0 for _ in range(rows)] for _ in range(cols)]
        elif data and isinstance(data[0], list):
            if byrow:
                rows, cols = len(data), len(data[0])
                self._data = [[data[i][j] for i in range(rows)]
                              for j in range(cols)]
            else:
                self._data = deepcopy(data)
        else:
            if byrow:
                self._data = [[data[i * cols + j] for i in range(rows)]
                              for j in range(cols)]
            else:
                self._data = [[data[i * rows + j] for j in range(rows)]
                              for i in range(cols)]

    @staticmethod
    def identity(dimensions):
        """Factory method for identity Matrix."""
        return Matrix(data=[[int(i == j) for i in range(dimensions)]
                            for j in range(dimensions)])

    @property
    def columns(self) -> int:
        """Number of columns."""
        return len(self._data)

    @property
    def rows(self) -> int:
        """Number of rows."""
        return len(self._data[0])

    def column(self, number: int) -> Generator[Number, None, None]:
        """Get all elements from a column."""
        yield from self._data[number]

    def row(self, number: int) -> Generator[Number, None, None]:
        """Get all elements from a row."""
        yield from (col[number] for col in self._data)

    def scalar_multiplication(self, escalar: Number) -> 'Matrix':
        """Returns the Matrix multiplied by a scalar."""
        data = [[i * escalar for i in col] for col in self._data]
        return Matrix(data=data)

    def dot_product(self, vector: List[Number], number: int = 0,
                    row=True) -> Number:
        """Dot product of a row or column by a vector."""
        if row:
            res = [col[number] * num for col, num in zip(self._data, vector)]
        else:
            res = [i * num for i, num in zip(self._data[number], vector)]
        return sum(res)

    def product(self, other: 'Matrix') -> 'Matrix':
        """Matrix product by another Matrix."""
        assert self.columns == other.rows
        data = [[sum(i * j for i, j in zip(self.row(m), other.column(n)))
                 for m in range(self.rows)] for n in range(other.columns)]
        return Matrix(data=data)

    def transposed(self) -> 'Matrix':
        """Transposed Matrix."""
        data = [[i for i in self.row(j)] for j in range(self.rows)]
        return Matrix(data=data)

    def invert(self) -> 'Matrix':
        """Inverts the Matrix."""
        assert self.rows == self.columns
        self.extend_with_identity()
        self.to_row_echelon()
        for i, col in enumerate(islice(self._data, self.rows)):
            for j in range(i):
                self.add_rows(j, i, -(col[j] / col[i]))
        self._data = self._data[self.rows:]

    def inverse(self) -> 'Matrix':
        """Returns the iverted Matrix."""
        matrix = deepcopy(self)
        matrix.invert()
        return matrix

    def swap_rows(self, row1: int, row2: int):
        """Swap two rows."""
        for col in self._data:
            col[row1], col[row2] = col[row2], col[row1]

    def add_rows(self, row1: int, row2: int, mult: Number):
        """Add row2 multiplied by mult to row1."""
        for col in self._data:
            col[row1] += mult * col[row2]

    def multiply_row(self, row: int, mult: Number):
        """Multiplies row by scalar."""
        for col in self._data:
            col[row] *= mult

    def extend_with_identity(self):
        """Extend matrix to the right with and identity matrix."""
        for i in range(self.rows):
            self._data.append([int(c == i) for c in range(self.rows)])

    def to_row_echelon(self, reduced=True):
        """Transform to row echelon form."""
        for piv in range(min(self.rows, self.columns)):
            i_max, _ = max((p for p in islice(
                enumerate(self.column(piv)), piv, None)),
                           key=lambda x: abs(x[1]))
            col = self._data[piv]
            if col[i_max] == 0:
                raise ZeroDivisionError(
                    'Cannot transform to row echelon form.')
            self.swap_rows(piv, i_max)
            for i in range(piv + 1, self.rows):
                self.add_rows(i, piv, -(col[i] / col[piv]))
        if reduced:
            for piv in range(min(self.rows, self.columns)):
                self.multiply_row(piv, 1 / self._data[piv][piv])

    def elementwise_operation(self, other: 'Matrix', operation: Callable
                              ) -> 'Matrix':
        """Applies an operation between each two corresponding elements in the
        two matrices.
        """
        return Matrix(
            data=[[operation(a, b) for a, b in zip(c1, c2)] for c1, c2 in zip(
                (self.column(i) for i in range(self.columns)),
                (other.column(j) for j in range(other.columns)))])

    def __abs__(self):
        data = deepcopy(self._data)
        for col in data:
            col[:] = map(abs, col)
        return Matrix(data=data)

    def __add__(self, other):
        return self.elementwise_operation(other, add)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return isinstance(other, Matrix) and other == self._data
        if other == 0:
            return all(i == 0 for i in chain.from_iterable(self._data))
        return self._data == other

    def __getitem__(self, key):
        return self._data[key[1]][key[0]]

    def __iter__(self):
        return (a for a in chain.from_iterable(self._data))

    def __neg__(self):
        data = deepcopy(self._data)
        for col in data:
            col[:] = map(lambda x: -x, col)
        return Matrix(data=data)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.elementwise_operation(other, mul)
        return self.scalar_multiplication(other)

    def __repr__(self):
        return f'Matrix(data={str(self._data)})'

    def __rmul__(self, other):
        return self.scalar_multiplication(other)

    def __round__(self, ndigits=None):
        data = deepcopy(self._data)
        for col in data:
            col[:] = map(partial(round, ndigits=ndigits), col)
        return Matrix(data=data)

    def __setitem__(self, key, value):
        if not isinstance(value, Number):
            raise ValueError('Value must be a number.')
        self._data[key[1]][key[0]] = value

    def __sub__(self, other):
        return self.elementwise_operation(other, sub)

    def __str__(self):
        return str(self._data)
