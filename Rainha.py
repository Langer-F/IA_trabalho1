import numpy as np

"""Intuito de ser hashable"""


class Tabuleiro:
    def __init__(self, tabuleiro) -> None:
        self.tabuleiro = tabuleiro

    def acha_posicao_rainhas(self) -> np.array:
        linhas, colunas = np.shape(self.tabuleiro)
        rainhas = []
        for i in range(linhas):
            for j in range(colunas):
                if self.tabuleiro[i, j] == 1:
                    rainhas.append((i, j))
        return np.array(rainhas)

    def acha_todas_posicoes_possiveis_de_rainha(self, rainha) -> list:
        linhas, colunas = np.shape(self.tabuleiro)

        posicoes = []
        for i in range(linhas):
            posicoes.append((i, rainha[1]))
            posicoes.append((rainha[0], i))

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


    def n_rainhas_busca_em_largura(self):
        tabuleiros_a_expandir = self.acha_todas_movimentacoes_possiveis_de_rainhas()
        visited = {}

        while tabuleiros_a_expandir:
            if len(tabuleiros_a_expandir) == 0:
                print(tabuleiros_a_expandir)
            tabuleiro: Tabuleiro = tabuleiros_a_expandir.pop(0)
            visited[tabuleiro.to_string()] = tabuleiro

            if self.calcula_custo() == 0:
                return visited

            for proximo_a_inserir in self.acha_todas_movimentacoes_possiveis_de_rainhas():
                if visited.get(proximo_a_inserir.to_string()) is None:
                    tabuleiros_a_expandir.append(proximo_a_inserir)
                    

        return visited


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


def main():
    tabuleiro = Tabuleiro.cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(4)

    print(tabuleiro.tabuleiro)
    # print(acha_todas_posicoes_possiveis_de_rainhas(tabuleiro))
    print(tabuleiro.n_rainhas_busca_em_largura())


if __name__ == '__main__':
    main()
