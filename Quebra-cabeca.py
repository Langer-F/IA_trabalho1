import unittest
import numpy as np
from problema_de_ia import Estado 

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
    def calcula_heuristica(self) -> int:
        return super().calcula_heuristica()

    def calcula_custo_transicao(self) -> int:
        if self.origem is None:
            return 0
        

        

    def generate_initial_boards(n):
        board1 = 'B' * n + 'X' + 'P' * n
        board2 = 'P' * n + 'X' + 'B' * n
        return QuebraCabeca(board1), QuebraCabeca(board2)
    
    def generate_all_initial_boards():
        boards = []
        for i in range(3, 5+1):
            boards += QuebraCabeca.generate_initial_boards(i)
        return boards

    def acha_n(self) -> int:
        return len(self.tabuleiro) // 2

    def gera_movimentos_possiveis(self):
        """
        - Fichas podem *pular* ou *deslizar* para a posição vazia,
        quando a ela estiver distante de no máximo N casas
        - O deslize ocorre quando a ficha está ao lado da posição vazia
        - No máximo 2N movimentos legais (se vazio no meio da bandeja)
        - Custo de um pulo (ou deslize se for imediato) é a distância até o vazio.
        """

        todos_movimentos_possiveis = []
        posicao_do_x = self.tabuleiro.index('X')

        n = self.acha_n()
        minima_posicao_a_esquerda = max(0, posicao_do_x - n)
        minima_posicao_a_direita = min(len(self.tabuleiro), posicao_do_x + n)

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
        return QuebraCabeca.eh_estado_final_estatico(list(self.tabuleiro))

    def eh_estado_final_estatico(state):
        """
        Objetivo: todas as fichas brancas no meio das pretas ou o contrário,
        estando a posição vazia à esquerda ou à direita (4 estados finais)
        """

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

class QuebraCabecaTest(unittest.TestCase):
    def test_goal(self):
        self.assertTrue(QuebraCabeca.eh_estado_final_estatico(list("PBBBPPX")))
        self.assertTrue(QuebraCabeca.eh_estado_final_estatico(list("XPBBBPP")))
        self.assertTrue(QuebraCabeca.eh_estado_final_estatico(list("BPPPBBX")))
        self.assertTrue(QuebraCabeca.eh_estado_final_estatico(list("XBPPPBB")))
        self.assertFalse(QuebraCabeca.eh_estado_final_estatico(list("PBBXBPP")))
        self.assertFalse(QuebraCabeca.eh_estado_final_estatico(list("XPBBPBP")))
        self.assertFalse(QuebraCabeca.eh_estado_final_estatico(list("PBXBBPP")))
        self.assertFalse(QuebraCabeca.eh_estado_final_estatico(list("PXBBBPP")))
    
    def test_dfs(self):
        for quebra_cabeca in QuebraCabeca.generate_all_initial_boards():
            tabuleiro_final, dfs_result = quebra_cabeca.busca_em_profundidade_iterativa()

            self.assertEqual(dfs_result, True)

    def test_bfs(self):
        for quebra_cabeca in QuebraCabeca.generate_all_initial_boards():
            tabuleiro_final, result = quebra_cabeca.busca_em_largura()

            self.assertEqual(result, True)

    def test_subida_de_encosta(self):
        for quebra_cabeca in QuebraCabeca.generate_all_initial_boards():
            tabuleiro_final, result = quebra_cabeca.subida_de_encosta()

            self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()