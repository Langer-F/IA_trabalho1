import numpy as np
import time
import unittest
from problema_de_ia import Estado 
import timeout_decorator

LOCAL_TIMEOUT = 150

class Tabuleiro(Estado):
    def __init__(self, tabuleiro, origem=None) -> None:
        super().__init__(np.array(tabuleiro), origem)

    def calcula_custo_de_transicao(self) -> int:
        return self.avalia_custo_do_estado_atual() # sabemos que não é, mas aqui não faz sentido não ser.

    def calcula_custo_desde_o_inicio(self) -> int:
        if self.origem is None:
            return 0
        return 1 + self.origem.calcula_custo_desde_o_inicio()

    def eh_estado_final(self) -> bool:
        return self.avalia_custo_do_estado_atual() == 0

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

    def gera_movimentos_possiveis_deste(self) -> list:
        tabuleiros_a_expandir = []
        for rainha in self.acha_posicao_rainhas():
            for posicao in self.acha_todas_posicoes_possiveis_de_rainha(rainha):
                tabuleiros_a_expandir.append(
                    self.move_rainha_em_novo_tabuleiro(rainha, posicao))
        return tabuleiros_a_expandir

    def move_rainha_em_novo_tabuleiro(self, inicio: tuple, destino: tuple):
        (linha_inicio, coluna_inicio) = inicio
        (linha_destino, coluna_destino) = destino
        novo_tabuleiro = Tabuleiro(self.tabuleiro, self)
        novo_tabuleiro.tabuleiro[linha_destino, coluna_destino], novo_tabuleiro.tabuleiro[linha_inicio][coluna_inicio] = novo_tabuleiro.tabuleiro[
            linha_inicio][coluna_inicio], novo_tabuleiro.tabuleiro[linha_destino, coluna_destino]
        return novo_tabuleiro

    def move_rainha_de_linha(self, inicio: tuple, destino: tuple):
        assert inicio[1] == destino[1]
        return self.move_rainha_em_novo_tabuleiro(inicio=inicio, destino=destino)

    def move_rainha_de_coluna(self, inicio: tuple, destino: tuple):
        assert inicio[0] == destino[0]
        return self.move_rainha_em_novo_tabuleiro(inicio=inicio, destino=destino)
    
    def calcula_heuristica(self) -> int:
        return self.avalia_custo_do_estado_atual()

    def avalia_custo_do_estado_atual(self):
        """Diferentemente do custo de transicao comum, aqui é mais importante considerar quantas peças estão se atacando"""
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
    def calcula_custo_desde_o_inicio(self) -> int:
        if self.origem is None:
            return 0
        return 1 + self.origem.calcula_custo_desde_o_inicio()
    def cria_tabuleiro_nxn_inicial_sem_linha_nem_coluna_repetida(n: int):
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


class Testbfs(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def test_bfs_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_bfs_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)

    #@unittest.skip("TODO")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)

    #@unittest.skip("TODO")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)
        
    #@unittest.skip("TODO")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)

    #@unittest.skip("TODO")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.busca_em_largura()
        self.assertEqual(result[1], True)


#@unittest.skip("grandes e não determinísticos...")
class UniformeTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.busca_de_custo_uniforme()
        self.assertEqual(result[1], True)


@unittest.skip("Feito")
class DfsTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def test_dfs_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_dfs_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_dfs_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_dfs_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_dfs_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    def test_dfs_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_dfs_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.busca_em_profundidade_iterativa()
        self.assertEqual(result[1], True)

@unittest.skip("FEITO")
class SubidaDeEncostaTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def test_subida_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_subida_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_subida_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_subida_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_subida_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    def test_subida_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_subida_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.subida_de_encosta()
        self.assertEqual(result[1], True)


@unittest.skip("Feito")
class SimulatedAnnealingTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def test_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    def test_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

    #@unittest.skip("Feito")
    def test_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.simulated_annealing()
        self.assertEqual(result[1], True)

@unittest.skip("Feito")
class A_estrela_test(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def test_a_estrela_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.busca_a_estrela()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_a_estrela_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.busca_a_estrela()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_a_estrela_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_a_estrela()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    def test_a_estrela_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.busca_a_estrela()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def test_a_estrela_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.busca_a_estrela()
        self.assertEqual(result[1], True)


@unittest.skip("Feito")
@unittest.skip("Feito")
class SubidaDeEncostaReinicioAleatorioTest(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    @unittest.skip("Feito")
    def teste_subida_reinicio_aleatorio_4(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,1],
            [0,0,0,1],
            [0,0,1,0],
            [1,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def teste_subida_reinicio_aleatorio_5(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [1,0,0,0,0],
            [0,0,1,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    def teste_subida_reinicio_aleatorio_6(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,1],
            [0,0,0,0,0,1],
            [0,0,0,1,0,0],
            [1,0,0,0,0,0],
            [0,0,1,0,0,0],
            [0,1,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def teste_subida_reinicio_aleatorio_7(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0],
            [1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0],
            [0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def teste_subida_reinicio_aleatorio_8(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)
        
    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def teste_subida_reinicio_aleatorio_9(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,1],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)

    @unittest.skip("Feito")
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def teste_subida_reinicio_aleatorio_10(self):
        tabuleiro = Tabuleiro(np.array([
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0]
        ]))

        result = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
        self.assertEqual(result[1], True)



if __name__ == '__main__':
    unittest.main()
    # tabuleiro, conseguiu = Tabuleiro.cria_tabuleiro_inicial_aleatorio(
    #    4).busca_em_profundidade()

    # if conseguiu:
    #    print(tabuleiro.criar_caminho_string())

