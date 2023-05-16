import unittest
import numpy as np
from problema_de_ia import Estado 
from pprint import pprint
import time
import timeout_decorator
LOCAL_TIMEOUT = 150

class QuebraCabeca(Estado):
    """
    2) Quebra-cabeça das N fichas brancas e N pretas (2N fichas)
    - N entre 3 e 5 fichas de cada cor
    """

    """
    Algoritmos de busca que devem ser implementados:

    1. Busca Simples
        - Busca em Largura
        - Busca em Profundidade Iterativa;
        - Busca de Menor Custo (ou Busca de Custo Uniforme)

    2. Busca Informada
        - Busca A*

    3. Busca Local
        - Subida de Encosta (hill climbing)
        - Subida de Encosta (hill climbing) com reinício aleatório
        - Têmpora Simulada (Simulated Annealing)
    """

    """
    Observações Importantes:
        C) Nos algoritmos de busca local, apresentar a sequência de passos

        D) Nos algoritmos de busca em árvore, manter registro dos
        estados já visitados.

        E) Para cada experimento, o programa deve imprimir (por exemplo):

        Solução: BBXPP-BBPXP-BXPBP-BPXBP-XPBBP
        número de nós visitados: ........ 20
        profundidade da meta: ............ 4
        custo da solução: ................ 6
    """

    def avalia_custo_do_estado_atual(self) -> int:
        return self.calcula_heuristica()

    def gera_estados_finais(self) -> list:
        estados_finais_sem_espacos_ps = list()

        n = self.acha_n() 
        p_no_inicio = n - 1

        while p_no_inicio > 0:
            estados_finais_sem_espacos_ps.append(list('P' * p_no_inicio + 'B' * n + 'P' * (n - p_no_inicio)))
            p_no_inicio -= 1

        estados_finais_sem_espacos = list(estados_finais_sem_espacos_ps)

        for estado_final_so_com_ps_no_inicio in estados_finais_sem_espacos_ps:
            estado_com_bs = ['P' if letra != 'P' 
                             else 'B' 
                             for letra in estado_final_so_com_ps_no_inicio] 
            estados_finais_sem_espacos.append(estado_com_bs)
        
        estados_finais = list()

        for estado_sem_espaco in estados_finais_sem_espacos:
            estados_finais.append(['X'] + estado_sem_espaco)
            estados_finais.append(estado_sem_espaco + ['X'])
        
        return estados_finais


    def calcula_heuristica(self) -> int:
        menor_distancia_para_estado_final = float('inf')

        for estado_final in self.gera_estados_finais():
            custo_ate_estado_final = 0
            for posicao, ficha in enumerate(estado_final):
                if self.tabuleiro[posicao] != ficha:
                    custo_ate_estado_final += 1
            menor_distancia_para_estado_final = min(menor_distancia_para_estado_final, custo_ate_estado_final)

        return int(menor_distancia_para_estado_final)
    
    def calcula_custo_de_transicao(self) -> int:
        if self.origem is None:
            return 0
        
        distance = float('inf')
        somar = False
        for i, ficha in enumerate(self.tabuleiro):
            if ficha != self.origem.tabuleiro[i]:
                if somar:
                    distance += i
                    return distance
                else:
                    distance = -i
                    somar = True
        
        return distance

    def generate_initial_boards(n):
        board1 = 'B' * n + 'X' + 'P' * n
        board2 = 'P' * n + 'X' + 'B' * n
        return QuebraCabeca(list(board1)), QuebraCabeca(list(board2))
    
    def generate_all_initial_boards():
        boards = []
        for i in range(3, 5+1):
            boards += QuebraCabeca.generate_initial_boards(i)
        return boards

    def acha_n(self) -> int:
        return len(self.tabuleiro) // 2

    def gera_movimentos_possiveis_deste(self):
        todos_movimentos_possiveis = []
        posicao_do_x = self.tabuleiro.index('X')

        n = self.acha_n()
        minima_posicao_a_esquerda = max(0, posicao_do_x - n)
        minima_posicao_a_direita = min(len(self.tabuleiro), posicao_do_x + n + 1)

        inseridos = {}

        for i in range(minima_posicao_a_esquerda, minima_posicao_a_direita):
            if i == posicao_do_x:
                continue

            copia_tabuleiro = list(self.tabuleiro)
            copia_tabuleiro[i], copia_tabuleiro[posicao_do_x] = copia_tabuleiro[posicao_do_x], copia_tabuleiro[i]
        
            if inseridos.get(str(copia_tabuleiro)) is None:
                todos_movimentos_possiveis.append(QuebraCabeca(copia_tabuleiro, self))
                inseridos[str(copia_tabuleiro)] = True
        
        return todos_movimentos_possiveis


    def eh_estado_final(self):
        return QuebraCabeca.eh_estado_final_estatico(self.tabuleiro)

    def eh_estado_final_estatico(state):
        if len(state) == 0:
            return False

        if state.count('X') != 1:
            return False
        
        if state[0] != 'X' and state[-1] != 'X':
            return False
        
        if state[0] == 'X':
            state = state[1:]
        else:
            state = state[:-1]
        
        primeiro_bloco = state[0]
        segundo_bloco = None

        while len(state) > 0 and state[0] == primeiro_bloco:
            state.pop(0)

        if len(state) == 0:
            return False

        segundo_bloco = state[0]
        terceiro_bloco = None

        while len(state) > 0 and state[0] == segundo_bloco:
            state.pop(0)
        
        if len(state) == 0:
            return False

        terceiro_bloco = state[0]

        while len(state) > 0:
            elemento_do_terceiro_bloco = state.pop(0)
            if elemento_do_terceiro_bloco != terceiro_bloco:
                return False
        
        return True

class Testbfs(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.busca_em_largura()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.busca_em_largura()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_bfs_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.busca_em_largura()
        self.assertTrue(resultado[1])

class Testprofu(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_dfs_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.busca_em_profundidade_iterativa()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_dfs_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.busca_em_profundidade_iterativa()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_dfs_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.busca_em_profundidade_iterativa()
        self.assertTrue(resultado[1])

class Testsubida(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.subida_de_encosta()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.subida_de_encosta()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.subida_de_encosta()
        self.assertTrue(resultado[1])

class Testbusca_a_estrela(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_busca_a_estrela_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.busca_a_estrela()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_busca_a_estrela_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.busca_a_estrela()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_busca_a_estrela_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.busca_a_estrela()
        self.assertTrue(resultado[1])

class Testsubidaaleatoria(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_al_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.subida_de_encosta_com_reinicio_aleatorio()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_al_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.subida_de_encosta_com_reinicio_aleatorio()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_subida_al_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.subida_de_encosta_com_reinicio_aleatorio()
        self.assertTrue(resultado[1])

class Testuniforme(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.busca_de_custo_uniforme()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.busca_de_custo_uniforme()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_uniforme_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.busca_de_custo_uniforme()
        self.assertTrue(resultado[1])   

class TestSimulated(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_simulated_3(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(3)[0]
        resultado = quebracabeca.simulated_annealing()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_simulated_4(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(4)[1]
        resultado = quebracabeca.simulated_annealing()
        self.assertTrue(resultado[1])

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_simulated_5(self):
        quebracabeca = QuebraCabeca.generate_initial_boards(5)[1]
        resultado = quebracabeca.simulated_annealing()
        self.assertTrue(resultado[1])   

if __name__ == '__main__':
    unittest.main()
    """
    # avaliando gera_estados_finais
    estado_n_2 = QuebraCabeca(['P', 'B', 'P', 'B', 'X'])
    pprint(estado_n_2.gera_estados_finais())
    estado_n_3 = QuebraCabeca(['P', 'B', 'P', 'P', 'B', 'B', 'X'])
    pprint(estado_n_3.gera_estados_finais())
    pprint(estado_n_3.calcula_heuristica())
    estado_n_4 = QuebraCabeca(['P', 'B', 'P', 'P','B', 'B', 'X', 'B', 'P',])
    pprint(estado_n_4.gera_estados_finais())
    """