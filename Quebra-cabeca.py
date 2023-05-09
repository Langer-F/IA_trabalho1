import numpy as np

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



def generate_children(state):
    """
    - Fichas podem *pular* ou *deslizar* para a posição vazia,
    quando a ela estiver distante de no máximo N casas
    - O deslize ocorre quando a ficha está ao lado da posição vazia
    - No máximo 2N movimentos legais (se vazio no meio da bandeja)
    - Custo de um pulo (ou deslize se for imediato) é a distância até o vazio.
    """

    n = len(state) // 2
    empty_pos = state.index('0')
    children = []
    
    for i in range(len(state)):
        if state[i] != 0 and abs(i - empty_pos) <= n:
            # calcula a distância entre a posição atual da peça e a posição vazia
            dist = abs(i - empty_pos)
            # verifica se a peça pode pular para a posição vazia
            if dist > 1:
                new_state = list(state)
                new_state[i], new_state[empty_pos] = new_state[empty_pos], new_state[i]
                cost = dist
                children.append((tuple(new_state), cost))
            # verifica se a peça pode deslizar para a posição vazia
            elif dist == 1:
                if empty_pos > i:
                    new_state = list(state)
                    new_state[empty_pos -
                              1], new_state[empty_pos] = new_state[empty_pos], new_state[empty_pos - 1]
                    cost = dist
                    children.append((tuple(new_state), cost))
                else:
                    new_state = list(state)
                    new_state[empty_pos +
                              1], new_state[empty_pos] = new_state[empty_pos], new_state[empty_pos + 1]
                    cost = dist
                    children.append((tuple(new_state), cost))
    return children

def is_goal(state):
    """
    Objetivo: todas as fichas brancas no meio das pretas ou o contrário,
    estando a posição vazia à esquerda ou à direita (4 estados finais)
    """

    n = len(state) // 2
    str = ''.join(state)
    bloco_b = 'B' * n
    bloco_p = 'P' * n
    blocos = (bloco_b, bloco_p)

    # Verifica se a posição vazia está à esquerda ou à direita
    if state[0] == 'X' or state[-1] == 'X':
        # Temos um bloco
        if bloco_b or bloco_p in str:
            # Bloco não está na borda
            if not (str.startswith(blocos) or str.endswith(blocos)):
                # Bloco não está ao lado do X - equivalente a termos os 2 tipos de blocos
                if not (bloco_b and bloco_p in str):
                    return True
    
    return False
