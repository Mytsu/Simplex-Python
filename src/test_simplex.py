import unittest
from itertools import islice

from matrix import Matrix
from simplex import Simplex


class TestSimplex(unittest.TestCase):

    def teste_um(self):
        A = [[0.2, 1, 2], [-0.8, 0, 4], [0, 1, 0], [0, 0, 1],
             [-1, 0, 0], [1, 0, 0]]
        b = [0, 100, 240]
        c = [-20, -50, 0, 0, 0, 1000]
        simplex = Simplex(A, b, c)
        simplex.run()
        expected = Matrix(data=[[80, 20]])
        result = Matrix(data=[list(islice(simplex.solution, 2))])
        self.assertAlmostEqual(result, expected)

    def teste_dois(self):
        A = [[8, 5, 5], [5, 4, 4], [4, 2, 2], [1, 0, 0], [0, 1, 0],
             [0, 1, -1], [0, 0, 1]]
        b = [120, 200, 140]
        c = [-20, -22, -18, 0, 0, 0, 10000]
        simplex = Simplex(A, b, c)
        simplex.run()
        self.fail('Cadê o teste?')

    def teste_tres(self):
        A = [[6, 1, -1, 0], [4, 2, 1, 1], [1, 0, 0, 0], [0, 1, 0, 0],
             [0, 0, 1, 0], [0, 0, 0, 1]]
        b = [24, 6, 1, 2]
        c = [-5, -4, 0, 0, 0, 0]
        simplex = Simplex(A, b, c)
        simplex.run()
        expected = Matrix(data=[[3, 1.5]])
        result = Matrix(data=[list(islice(simplex.solution, 2))])
        self.assertAlmostEqual(result, expected)

    def teste_quatro(self):
        A = [[1, 0, 1, 2], [0, 1, 1, 3], [-1, 0, 0, 0], [0, -1, 0, 0],
             [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]
        b = [20, 30, 12000, 10000]
        c = [-20, -35, 0, 0, 0, 0, 100000, 100000]
        simplex = Simplex(A, b, c)
        simplex.run()
        expected = Matrix(data=[[20, 3320]])
        result = Matrix(data=[list(islice(simplex.solution, 2))])
        self.assertAlmostEqual(result, expected)

    def teste_cinco(self):
        A = [[1, 2], [1, 1], [1, 3], [1, 0], [0, 1]]
        b = [30, 60]
        c = [-2, -3, -4, 0, 1000]
        simplex = Simplex(A, b, c)
        simplex.run()
        expected = Matrix(data=[[0, 15, 15]])
        result = Matrix(data=[list(islice(simplex.solution, 3))])
        self.assertAlmostEqual(result, expected)

    def teste_seis(self):
        A = [[8, 5, 0.7], [5, 10, 1], [2, 4, 2],
             [1, 0, 0], [0, 1, 0], [0, 0, 1]]
        b = [120, 400, 80]
        c = [-1, -1.5, -2, 0, 0, 0]
        simplex = Simplex(A, b, c)
        simplex.run()
        expected = Matrix(data=[[0, 10, 35]])
        result = Matrix(data=[list(islice(simplex.solution, 3))])
        self.assertAlmostEqual(result, expected)


'''
min -2*x1 - 3*x2 - 4*x3 - 1000000

R1:   x1 + x2 +   x3 + x4      = 30;
R2: 2*x1 + x2 + 3*x3      + y1 = 60;
'''


if __name__ == "__main__":
    unittest.main()
