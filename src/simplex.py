from numbers import Number
from typing import List, Tuple, Union

from matrix import Matrix


class Simplex:

    N_DIGITS = 5

    def __init__(self,
                 A: Union[List[List[Number]], Matrix],
                 b: Union[List[Number], Matrix],
                 c: Union[List[Number], Matrix]):

        if isinstance(A, Matrix):
            self.coefficients = A
        else:
            self.coefficients = Matrix(data=A)

        if isinstance(b, Matrix):
            self.resources = b
        else:
            self.resources = Matrix(len(b), 1, b)

        if isinstance(c, Matrix):
            self.cost = c
        else:
            self.cost = Matrix(1, len(c), c)

        self.variables = self.coefficients.columns
        self.restrictions = self.coefficients.rows
        self.base_variables = [None for _ in range(self.restrictions)]
        self.multiple_solutions = False
        self.solution: Matrix
        self.second_solution: Matrix
        self.base: Matrix
        self.base_inv: Matrix
        self.reduced_cost: List[Number]
        self.direction: List[Number]

    def run(self):

        self.initial_bfs()
        self.update_base()

        enter = self.next_to_enter_base()
        while enter is not None:
            self.direction = self.get_direction(enter)
            if all(x >= 0 for x in self.direction):
                break
            self.new_bfs(self.direction, enter)
            if self.multiple_solutions:
                break
            self.update_base()
            enter = self.next_to_enter_base()

    def initial_bfs(self):
        for col in range(self.variables):
            if self.can_be_base(col) and col not in self.base_variables:
                i = list(self.coefficients.column(col)).index(1)
                self.base_variables[i] = col
        assert all(x is not None for x in self.base_variables)
        self.solution = Matrix(
            data=[[0 if i not in self.base_variables
                   else self.resources[self.base_variables.index(i), 0]
                   for i in range(self.variables)]])

    def update_base(self) -> Matrix:
        data = [list(self.coefficients.column(i)) for i in self.base_variables]
        self.base = Matrix(len(data), len(data[0]), data)
        self.base_inv = self.base.inverse()

    def can_be_base(self, i: int) -> bool:
        """Checks if column can be part of base."""
        return all(j in (0, 1) for j in self.coefficients.column(i)) and \
            list(self.coefficients.column(i)).count(1) == 1

    def next_to_enter_base(self) -> List:
        """Get the index of the column that will enter to the base."""
        reduced_cost = round(self.cost - self.base_cost.transposed().product(
            self.base_inv.product(self.coefficients)), Simplex.N_DIGITS)
        self.reduced_cost = reduced_cost

        entering = next((i for i, k in enumerate(reduced_cost) if k < 0), None)
        if entering is not None:
            return entering

        entering, cost = next(
            ((i, k) for i, k in enumerate(reduced_cost)
             if k <= 0 and i not in self.base_variables), (None, None))
        if cost == 0:
            self.multiple_solutions = True
            self.second_solution = self.solution.copy()
        return entering

    @property
    def base_cost(self) -> Matrix:
        data = [self.cost[0, i] for i in self.base_variables]
        return Matrix(data=[data])

    def get_direction(self, entering: int) -> Matrix:
        base_dir = -self.base_inv.product(
            Matrix(data=[list(self.coefficients.column(entering))]))
        direction = [1 if i == entering else 0 if i not in self.base_variables
                     else base_dir[self.base_variables.index(i), 0]
                     for i in range(self.variables)]
        return Matrix(data=[direction])

    def get_leaving_variable(self, direction: Matrix) -> Tuple[Number, int]:
        return min([(abs(x/d), i) for i, (x, d) in
                    enumerate(zip(self.solution, direction)) if d < 0])

    def new_bfs(self, direction: Matrix, enter: int):
        step, leave = self.get_leaving_variable(direction)
        leave_index = self.base_variables.index(leave)
        self.solution = direction * step + self.solution
        self.base_variables[leave_index] = enter
