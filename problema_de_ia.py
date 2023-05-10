import numpy as np

LIMITE_SUBIDA_DE_ENCOSTA = 100

class Estado:
    def __init__(self, tabuleiro, origem=None):
        self.tabuleiro = tabuleiro
        self.origem = origem

    def calcula_custo(self) -> int:
        pass

    def calcula_heuristica(self) -> int:
        pass

    def gera_movimentos_possiveis(self) -> list:
        pass

    def busca_em_profundidade(self) -> tuple:
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

                pilha_tabuleiros_a_expandir += tabuleiro_base.gera_movimentos_possiveis()
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

                pilha_tabuleiros_a_expandir += tabuleiro_base.gera_movimentos_possiveis()

        return (None, False)

    def busca_em_largura(self) -> tuple:
        estados_a_expandir = [self]
        visitados = {}

        while estados_a_expandir:
            estado: Estado = estados_a_expandir.pop(0)

            visitados[str(estado)] = estado

            if estado.calcula_custo() == 0:
                return (estado, True)

            for proximo_a_inserir in estado.gera_movimentos_possiveis():
                if visitados.get(str(proximo_a_inserir)) is None:
                    estados_a_expandir.append(proximo_a_inserir)

        return (None, False)

    def subida_de_encosta(self, limit=100) -> tuple:
        if self.calcula_custo() == 0:
            return (self, True)

        movimentos_possiveis = self.gera_movimentos_possiveis()

        menor_estado = self
        for movimento in movimentos_possiveis:
            if movimento.calcula_custo() <= menor_estado.calcula_custo():
                menor_estado = movimento

        if menor_estado == self or limit > LIMITE_SUBIDA_DE_ENCOSTA:
            return (self, False)

        new_limit = 0
        if menor_estado.calcula_custo() == self.calcula_custo():
            new_limit = limit + 1

        return menor_estado.subida_de_encosta(new_limit)

    def subida_de_encosta_com_reinicio_aleatorio(self, quantidade_a_subir: int=0) -> tuple:
        if self.calcula_custo() == 0:
            return (self, True)
        
        if quantidade_a_subir > 0:
            a_subir = self.origem if self.origem is not None else self

            movimentos_possiveis = a_subir.gera_movimentos_possiveis()

            a_subir = movimentos_possiveis[np.random.randint(len(movimentos_possiveis))]

            try:
                return a_subir.subida_de_encosta_com_reinicio_aleatorio(quantidade_a_subir-1)
            except RecursionError:
                return (self, False)

        movimentos_possiveis = self.gera_movimentos_possiveis()

        menor_estado = self
        for movimento in movimentos_possiveis:
            if movimento.calcula_custo() <= menor_estado.calcula_custo():
                menor_estado = movimento

        if menor_estado.calcula_custo() < self.calcula_custo():
            return menor_estado.subida_de_encosta_com_reinicio_aleatorio()
        
        return self.subida_de_encosta_com_reinicio_aleatorio(np.random.randint(100))


    def criar_caminho_string(self):
        caminho_ate_ele = "--- INICIO ---\n"

        if self.origem is not None:
            caminho_ate_ele = self.origem.criar_caminho_string()
            
        return caminho_ate_ele + str(self) + "\n\n"

    def __str__(self):
        return str(self.tabuleiro)