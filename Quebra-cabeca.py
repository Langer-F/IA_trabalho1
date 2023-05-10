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

    def generate_initial_boards():
        n = int(input("N: "))
        assert n >= 3 and n <= 5, "N deve ser entre 3 e 5"
        board1 = 'B' * n + 'X' + 'P' * n
        board2 = 'P' * n + 'X' + 'B' * n
        return board1, board2

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
        tabuleiro_final, dfs_result = QuebraCabeca(list("BBXPP")).busca_em_profundidade_iterativa()

        print(tabuleiro_final.criar_caminho_string())

        self.assertEqual(dfs_result, True)


if __name__ == '__main__':
    unittest.main()