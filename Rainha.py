import numpy as np
import unittest

class Tabuleiro:
    def __init__(self, tabuleiro) -> None:
        self.tabuleiro = np.array(tabuleiro)

    def acha_posicao_rainhas(self):
        linhas, colunas = np.shape(self.tabuleiro)
        rainhas = []
        for i in range(linhas):
            for j in range(colunas):
                if self.tabuleiro[i, j] == 1:
                    rainhas.append((i, j))
        return rainhas

    def acha_todas_posicoes_possiveis_de_rainha(self, rainha) -> list:
        linhas, colunas = np.shape(self.tabuleiro)

        posicoes = []
        for i in range(linhas):
            move_horizontal = (i, rainha[1])
            move_vertical = (rainha[0], i)
            if move_horizontal != rainha:
                if move_horizontal not in posicoes and self.tabuleiro[move_horizontal[0], move_horizontal[1]] == 0:
                    posicoes.append(move_horizontal)
            if move_vertical != rainha and self.tabuleiro[move_vertical[0], move_vertical[1]] == 0:
                posicoes.append(move_vertical)
                if move_vertical not in posicoes:
                    posicoes.append(move_vertical)

        return posicoes

    def acha_todas_movimentacoes_possiveis_de_rainhas(self) -> list:
        tabuleiros_a_expandir = []
        for rainha in self.acha_posicao_rainhas():
            for posicao in self.acha_todas_posicoes_possiveis_de_rainha(rainha):
                tabuleiros_a_expandir.append(
                    self.move_rainha_em_novo_tabuleiro(rainha, posicao))
        return tabuleiros_a_expandir

    def move_rainha_em_novo_tabuleiro(self, inicio: tuple, destino: tuple):
        (linha_inicio, coluna_inicio) = inicio
        (linha_destino, coluna_destino) = destino
        novo_tabuleiro = Tabuleiro(self.tabuleiro)
        novo_tabuleiro.tabuleiro[linha_destino, coluna_destino], novo_tabuleiro.tabuleiro[linha_inicio][coluna_inicio] = novo_tabuleiro.tabuleiro[
            linha_inicio][coluna_inicio], novo_tabuleiro.tabuleiro[linha_destino, coluna_destino]
        return novo_tabuleiro

    def move_rainha_de_linha(self, inicio: tuple, destino: tuple):
        assert inicio[1] == destino[1]
        return self.move_rainha_em_novo_tabuleiro(inicio=inicio, destino=destino)

    def move_rainha_de_coluna(self, inicio: tuple, destino: tuple):
        assert inicio[0] == destino[0]
        return self.move_rainha_em_novo_tabuleiro(inicio=inicio, destino=destino)

    def n_rainhas_busca_em_profundidade(self):
        pilha_tabuleiros_a_expandir = [self]

        visitados = {}

        LIMITE_PROFUNDIDADE = 10

        limitado = LIMITE_PROFUNDIDADE

        while pilha_tabuleiros_a_expandir:
            while limitado > 0:
                tabuleiro_base = pilha_tabuleiros_a_expandir.pop()

                if not visitados.get(str(tabuleiro_base)) is None:
                    continue

                if tabuleiro_base.calcula_custo() == 0:
                    return (tabuleiro_base, True)

                visitados[str(tabuleiro_base)] = tabuleiro_base

                pilha_tabuleiros_a_expandir += tabuleiro_base.acha_todas_movimentacoes_possiveis_de_rainhas()
                limitado -= 1

            limitado = LIMITE_PROFUNDIDADE
            copia_pilha = list(pilha_tabuleiros_a_expandir)

            while copia_pilha:
                tabuleiro_base = copia_pilha.pop(0)

                if not visitados.get(str(tabuleiro_base)) is None:
                    continue

                if tabuleiro_base.calcula_custo() == 0:
                    return (tabuleiro_base, True)

                visitados[str(tabuleiro_base)] = tabuleiro_base

                pilha_tabuleiros_a_expandir += tabuleiro_base.acha_todas_movimentacoes_possiveis_de_rainhas()

        return (None, False)

    def n_rainhas_busca_em_largura(self):
        tabuleiros_a_expandir = [self]
        visitados = {}

        while tabuleiros_a_expandir:
            tabuleiro: Tabuleiro = tabuleiros_a_expandir.pop(0)

            visitados[str(tabuleiro)] = tabuleiro

            if tabuleiro.calcula_custo() == 0:
                return (visitados, True)

            for proximo_a_inserir in tabuleiro.acha_todas_movimentacoes_possiveis_de_rainhas():
                if visitados.get(str(proximo_a_inserir)) is None:
                    tabuleiros_a_expandir.append(proximo_a_inserir)
                    
        return (visitados, False)


    def calcula_custo(self):
        """Dado um tabuleiro, calcula quantos pares de rainhas estão 'Se atacando'"""
        n = len(self.tabuleiro)
        custo = 0

        for i in range(n):
            for j in range(n):
                if self.tabuleiro[i][j] == 1:
                    for k in range(n):
                        if k != i:  # custo da linha
                            custo = custo + self.tabuleiro[k][j]
                        if k != j:  # custo da coluna
                            custo = custo + self.tabuleiro[i][k]
                        if k > 0:  # custo das diagonais
                            if (i+k) < n and (j+k) < n:
                                custo = custo + self.tabuleiro[i+k][j+k]
                            if (i+k) < n and (j-k) >= 0:
                                custo = custo + self.tabuleiro[i+k][j-k]
                            if (i-k) >= 0 and (j+k) < n:
                                custo = custo + self.tabuleiro[i-k][j+k]
                            if (i-k) >= 0 and (j-k) >= 0:
                                custo = custo + self.tabuleiro[i-k][j-k]
        return custo//2



    def cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(n: int):
        """Cria um tabuleiro NxN com N rainhas posicionadas, sendo que nenhuma linha ou coluna repete"""
        tabuleiro = np.zeros((n, n), dtype=int)
        for i in range(n):
            linha_ja_ocupada = True
            while linha_ja_ocupada:
                coluna = np.random.randint(0, n)
                linha_ja_ocupada = False
                for j in range(n):
                    if tabuleiro[j][coluna] == 1:
                        linha_ja_ocupada = True
                        break
            tabuleiro[i][coluna] = 1
        return Tabuleiro(tabuleiro)


    def cria_tabuleiro_inicial_aleatorio(n: int):
        """Cria um tabuleiro NxN com N rainhas posicionadas aleatoriamente, sem restrição (obviamente uma rainha nao pode ocupar uma casa já ocupada)"""
        tabuleiro = np.zeros((n, n), dtype=int)
        for _ in range(n):
            linha = np.random.randint(0, n)
            coluna = np.random.randint(0, n)
            while tabuleiro[linha][coluna] == 1:
                linha = np.random.randint(0, n)
                coluna = np.random.randint(0, n)
            tabuleiro[linha][coluna] = 1
        return Tabuleiro(tabuleiro)
    
    def __str__(self):
        return str(self.tabuleiro)


class Testbfs(unittest.TestCase):
    def test_pode_calcular_custos(self):
        tabuleiro = Tabuleiro(np.array([
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]))
        self.assertEqual(tabuleiro.calcula_custo(), 0)
        tabuleiro = Tabuleiro(np.array([
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]))
        self.assertEqual(tabuleiro.calcula_custo(), 2)

    def test_bfs_next(self):
        tabuleiro = Tabuleiro(np.array([
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]))

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)

        tabuleiro = Tabuleiro(np.array([
            [0, 0, 0, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]))

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)

        tabuleiro = Tabuleiro(np.array([
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 1, 0]
        ]))

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)

    def test_can_offer_reasonable_moves(self):
        tabuleiro = Tabuleiro(np.array([
            [0, 0],
            [1, 1],
        ]))

        self.assertListEqual(tabuleiro.acha_posicao_rainhas(), [
            (1, 0),
            (1, 1)
        ])

        tabuleiro = Tabuleiro(np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]))

        self.assertListEqual(tabuleiro.acha_posicao_rainhas(), [
                             (1, 0), (1, 1), (1, 2)])

    def test_bfs_distant(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            4)

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)

    """
    def test_bfs_5(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            5)

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)

    def test_bfs_6(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            6)

        bfs_result = tabuleiro.n_rainhas_busca_em_largura()
        self.assertEqual(bfs_result[1], True)
    """

    def test_dfs_distant(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            4)

        bfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(bfs_result[1], True)

    def test_dfs_5(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            5)

        bfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(bfs_result[1], True)

    """
    def test_dfs_6(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            6)

        bfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(bfs_result[1], True)

    def test_dfs_8(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            8)

        bfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(bfs_result[1], True)

    def test_dfs_10(self):
        tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(
            10)

        bfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(bfs_result[1], True)
    """

    def test_dfs_next(self):
        tabuleiro = Tabuleiro(np.array([
            [0, 0, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]))

        dfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(dfs_result[1], True)

        tabuleiro = Tabuleiro(np.array([
            [0, 0, 0, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ]))

        dfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(dfs_result[1], True)

        tabuleiro = Tabuleiro(np.array([
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 1, 0]
        ]))

        dfs_result = tabuleiro.n_rainhas_busca_em_profundidade()
        self.assertEqual(dfs_result[1], True)


if __name__ == '__main__':
    unittest.main()
