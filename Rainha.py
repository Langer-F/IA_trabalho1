import numpy as np


def acha_posicao_rainhas(tabuleiro) -> np.array:
    linhas, colunas = np.shape(tabuleiro)
    rainhas = []
    for i in range(linhas):
        for j in range(colunas):
            if tabuleiro[i, j] == 1:
                rainhas.append((i, j))
    return np.array(rainhas)


def acha_todas_posicoes_possiveis_de_rainha(tabuleiro, rainha) -> list:
    linhas, colunas = np.shape(tabuleiro)

    posicoes = []
    for i in range(linhas):
        posicoes.append((i, rainha[1]))
        posicoes.append((rainha[0], i))

    return posicoes


def acha_todas_posicoes_possiveis_de_rainhas(tabuleiro) -> list:
    tabuleiros_a_expandir = []
    for rainha in acha_posicao_rainhas(tabuleiro):
        for posicao in acha_todas_posicoes_possiveis_de_rainha(tabuleiro, rainha):
            tabuleiros_a_expandir.append(
                move_rainha(tabuleiro, rainha, posicao))
    return tabuleiros_a_expandir


def n_rainhas_busca_em_largura(tabuleiro_original):
    tabuleiros_a_expandir = acha_todas_posicoes_possiveis_de_rainhas(
        tabuleiro_original)
    primeira_geracao = True
    visited = []

    while tabuleiros_a_expandir or primeira_geracao:
        tabuleiro = tabuleiros_a_expandir.pop(0)
        visited.append(tabuleiro)

        if calcula_custo(tabuleiro) == 0:
            return visited

        for proximo_a_inserir in acha_todas_posicoes_possiveis_de_rainhas(tabuleiro):
            tabuleiros_a_expandir.append(proximo_a_inserir)

    return visited


def calcula_custo(tabuleiro):
    """Dado um tabuleiro, calcula quantos pares de rainhas estão 'Se atacando'"""
    n = len(tabuleiro)
    custo = 0

    for i in range(n):
        for j in range(n):
            if tabuleiro[i][j] == 1:
                for k in range(n):
                    if k != i:  # custo da linha
                        custo = custo + tabuleiro[k][j]
                    if k != j:  # custo da coluna
                        custo = custo + tabuleiro[i][k]
                    if k > 0:  # custo das diagonais
                        if (i+k) < n and (j+k) < n:
                            custo = custo + tabuleiro[i+k][j+k]
                        if (i+k) < n and (j-k) >= 0:
                            custo = custo + tabuleiro[i+k][j-k]
                        if (i-k) >= 0 and (j+k) < n:
                            custo = custo + tabuleiro[i-k][j+k]
                        if (i-k) >= 0 and (j-k) >= 0:
                            custo = custo + tabuleiro[i-k][j-k]
    return custo//2


def move_rainha(tabuleiro, inicio: tuple, destino: tuple):
    (linha_inicio, coluna_inicio) = inicio
    (linha_destino, coluna_destino) = destino
    tabuleiro[linha_destino, coluna_destino], tabuleiro[linha_inicio][coluna_inicio] = tabuleiro[
        linha_inicio][coluna_inicio], tabuleiro[linha_destino, coluna_destino]
    return tabuleiro


def move_rainha_de_linha(tabuleiro, inicio: tuple, destino: tuple):
    assert inicio[1] == destino[1]
    return move_rainha(tabuleiro=tabuleiro, inicio=inicio, destino=destino)


def move_rainha_de_coluna(tabuleiro, inicio: tuple, destino: tuple):
    assert inicio[0] == destino[0]
    return move_rainha(tabuleiro=tabuleiro, inicio=inicio, destino=destino)


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
    return tabuleiro


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
    return tabuleiro


def main():
    tabuleiro = cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(4)

    print(tabuleiro)
    # print(acha_todas_posicoes_possiveis_de_rainhas(tabuleiro))
    print(n_rainhas_busca_em_largura(tabuleiro))


if __name__ == '__main__':
    main()
