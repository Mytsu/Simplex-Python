import unittest
from matriz import Matriz


class TestMatriz(unittest.TestCase):

    def test_multiplica_escalar(self):
        matrix = Matriz(3, 3, [n + 1 for n in range(9)])
        result = matrix.multiplica_escalar(2)
        expected = Matriz(3, 3, [(n + 1) * 2 for n in range(9)])
        self.assertEqual(result, expected)

    def test_produto_escalar(self):
        matrix = Matriz(2, 3, [1, 2, 3, 4, 5, 6], byrow=True)
        result = matrix.produto_escalar([4, 3, 2], linha=True)
        self.assertEqual(result, 16)
        result = matrix.produto_escalar([5, 3], 1, linha=False)
        self.assertEqual(result, 25)

    def test_produto_matricial(self):
        matrix1 = Matriz(3, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8])
        matrix2 = Matriz(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = matrix1.produto_matricial(matrix2)
        expected = Matriz(3, 3, [24, 30, 36, 51, 66, 81, 78, 102, 126])
        self.assertEqual(result, expected)

    def test_transposta(self):
        matrix1 = Matriz(2, 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False)
        matrix2 = Matriz(5, 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True)
        self.assertEqual(matrix1.transposta(), matrix2)
        self.assertEqual(matrix2.transposta(), matrix1)


if __name__ == "__main__":
    unittest.main()
