"""Classe Matriz."""

from copy import deepcopy
from numbers import Number
from typing import Generator, List


class Matriz:
    """Implementação de matriz com diversas operações disponíveis."""
    def __init__(self, rows=None, cols=None, data=None, byrow=False):
        """Construtor de matrizes. Exemplos:

        Matriz(2, 3):
            0  0  0
            0  0  0

        Matriz(3, 2, [1, 2, 3, 4, 5, 6]):
            1  4
            2  5
            3  6

        Matriz(3, 2, [1, 2, 3, 4, 5, 6], byrow=True)
            1  2
            3  4
            5  6

        Matriz(data=[[1, 3], [5, 7]]):
            1  5
            3  7

        Matriz(data=[[1, 2, 3], [11, 12, 13]], byrow=True)
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

    @property
    def columns(self) -> int:
        """Número de colunas da matriz."""
        return len(self._data)

    @property
    def lines(self) -> int:
        """Número de linhas da matriz."""
        return len(self._data[0])

    def column(self, number: int) -> Generator[Number, None, None]:
        """Enumeração dos elementos de uma coluna."""
        yield from self._data[number]

    def line(self, number: int) -> Generator[Number, None, None]:
        """Enumeração dos elementos de uma linha."""
        yield from (col[number] for col in self._data)

    def multiplica_escalar(self, escalar: Number) -> 'Matriz':
        """Multiplica a matriz por um escalar, retorna a nova matriz sem
        alterar a anterior.
        """
        data = [[i * escalar for i in col] for col in self._data]
        return Matriz(data=data)

    def produto_escalar(self, vector: List[Number], number: int = 0,
                        linha=True) -> Number:
        """Multiplica uma linha ou coluna da matriz por um vetor"""
        if linha:
            res = [col[number] * num for col, num in zip(self._data, vector)]
        else:
            res = [i * num for i, num in zip(self._data[number], vector)]
        return sum(res)

    def produto_matricial(self, other: 'Matriz') -> 'Matriz':
        """Realiza o produto matricial por outra matriz."""
        assert self.columns == other.lines
        data = [[sum(i * j for i, j in zip(self.line(m), other.column(n)))
                 for m in range(self.lines)] for n in range(other.columns)]
        return Matriz(data=data)

    def transposta(self) -> 'Matriz':
        """Transpoe a matriz dada como entrada."""
        data = [[i for i in self.line(j)] for j in range(self.lines)]
        return Matriz(data=data)

    def inversa(self) -> 'Matriz':
        """Calcula a matriz inversa."""
        pass

    def __eq__(self, other):
        if isinstance(other, Matriz):
            return isinstance(other, Matriz) and other == self._data
        return self._data == other

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self._data)
