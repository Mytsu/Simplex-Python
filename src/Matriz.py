from copy import deepcopy


class Matriz(object):

    def __init__(self):
        pass

    # retorna o tamanho das linhas da matriz
    # @param m1 number[] - matriz
    def getM(self, m):
        return len(m)

    # retorna o tamanho das colunas da matriz (verifica apenas a primeira coluna)
    # @param m1 number[] - matriz
    def getN(self, m):
        return len(m[0])

    # multiplica a matriz por um escalar, retorna a nova matriz sem alterar a anterior
    # @param m1 number[] - matriz
    def multEscalar(self, m, e):
        mat = deepcopy(m)
        for i in range(mat):
            for j in range(mat):
                mat[i][j] *= e
        return mat

    # multiplica uma linha ou coluna da matriz por um vetor
    # retorna o valor encontrado
    # @param m number[] - matriz
    # @param v number[] - informa o vetor a ser multiplicado pelo vetor da matriz
    # @param n number - informa o índice do vetor da matriz
    # @param linha boolean - informa se deve buscar o vetor nas linhas ou colunas da matriz
    def prodEscalar(self, m, v, n=0, linha=True):
        # recupera o vetor a ser multiplicado
        if linha:
            # se for um vetor linha, apenas copia o vetor da matriz
            vet = deepcopy(self.matriz[n])
        else:
            # se for um vetor coluna, itera pelas linhas coletando os elementos do vetor
            vet = []
            for i in range(self.matriz):
                vet.append(self.matriz[i][n])
        for i in range(vet):
            vet[i] *= v[i]
        return vet

    # multiplica uma matriz m pela matriz na estrutura
    # @param m1 number[] - matriz 1
    # @param m2 number[] - matriz 2
    def prodMatricial(self, m1, m2):
        linhas1, colunas1 = (len(m1[0], len(m1)))
        linhas2, colunas2 = (len(m2[0], len(m2)))
        assert linhas1 == colunas2
        r = []
        for i in range(linhas1):
            r.append([])
            for j in range(colunas2):
                r[i].append(0)
                for k in range(colunas1):
                    r[i][j] += m1[i][k] * m2[k][j]
        return r

    def transposta(self, m):
        assert len(m) == len(m[0])
        r = []
        for i in range(len(m)):
            r.append([])
            for j in range(len(m[0])):
                r[i].append(m[j][i])
        return r

    def inversa(self):
        pass