import unittest
from matrix import Matrix


class TestMatrix(unittest.TestCase):

    def test_scalar_multiplication(self):
        matrix = Matrix(3, 3, [n + 1 for n in range(9)])
        result = matrix.scalar_multiplication(2)
        expected = Matrix(3, 3, [(n + 1) * 2 for n in range(9)])
        self.assertEqual(result, expected)

    def test_dot_product(self):
        matrix = Matrix(2, 3, [1, 2, 3, 4, 5, 6], byrow=True)
        result = matrix.dot_product([4, 3, 2], row=True)
        self.assertEqual(result, 16)
        result = matrix.dot_product([5, 3], 1, row=False)
        self.assertEqual(result, 25)

    def test_product(self):
        matrix1 = Matrix(3, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8])
        matrix2 = Matrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = matrix1.product(matrix2)
        expected = Matrix(3, 3, [24, 30, 36, 51, 66, 81, 78, 102, 126])
        self.assertEqual(result, expected)

    def test_transposed(self):
        matrix1 = Matrix(2, 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False)
        matrix2 = Matrix(5, 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True)
        self.assertEqual(matrix1.transposed(), matrix2)
        self.assertEqual(matrix2.transposed(), matrix1)

    def test_inverse(self):
        matrix = Matrix.identity(4)
        inverse = matrix.inverse()
        self.assertEqual(matrix, inverse)
        matrix = Matrix(data=[[1, 0, 3], [2, 5, 1], [0, 2, 2]])
        inverse = matrix.inverse()
        self.assertAlmostEqual(matrix.product(inverse), Matrix.identity(3))
        matrix = Matrix(data=[[1, 2, 3], [4, 8, 12], [16, 32, 48]])
        with self.assertRaises(ZeroDivisionError):
            matrix.invert()


if __name__ == "__main__":
    unittest.main()
