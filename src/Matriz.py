from copy import deepcopy

class Matriz(object):

    def __init__(self, mat):
        # mat deve ser uma lista de listas de números, ou uma lista de tuplas de números
        self.matriz = mat

    # retorna o tamanho das linhas da matriz
    def getM(self):
        return len(self.matriz)

    # retorna o tamanho das colunas da matriz (verifica apenas a primeira coluna)
    def getN(self):
        return len(self.matriz[0])

    # altera a matriz por uma matriz m
    def setMatriz(self, m):
        self.matriz = m

    # multiplica a matriz por um escalar, retorna a nova matriz sem alterar a anterior
    def multEscalar(self, e):
        mat = deepcopy(self.matriz)
        for i in range(mat):
            for j in range(mat):
                mat[i][j] *= e
        return mat

#   multiplica uma linha ou coluna da matriz por um vetor
#   retorna o valor encontrado
#   @param linha: boolean - informa se deve buscar o vetor nas linhas ou colunas da matriz
#   @param n: number - informa o índice do vetor da matriz
#   @param v: number[] - informa o vetor a ser multiplicado pelo vetor da matriz
    def prodEscalar(self, linha, n, v):
        e = 0
        # recupera o vetor a ser multiplicado
        if linha:
            # se for um vetor linha, apenas copia o vetor da matriz
            vet = deepcopy(self.matriz[n])
        else:
            # se for um vetor coluna, itera pelas linhas coletando os elementos do vetor
            vet = []
            for i in range(self.matriz):
                vet.append(self.matriz[i][n])

    def prodMatricial(self):
        pass

    def transposta(self):
        pass

    def inversa(self):
        pass