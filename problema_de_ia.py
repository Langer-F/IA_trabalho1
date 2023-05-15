import numpy as np
from random import choice

LIMITE_SUBIDA_DE_ENCOSTA = 100

class Estado:
    def __init__(self, tabuleiro, origem=None, limite_repeticoes_subida_de_encosta=LIMITE_SUBIDA_DE_ENCOSTA):
        self.tabuleiro = tabuleiro
        self.origem = origem
        self.limite_repeticoes_subida_de_encosta = limite_repeticoes_subida_de_encosta

    def eh_estado_final(self) -> bool:
        pass

    def avalia_custo_do_estado_atual(self) -> int:
        pass

    def calcula_custo_de_transicao(self) -> int:
        if self.origem is None:
            return 0
        return 1

    def calcula_custo_desde_o_inicio(self) -> int:
        if hasattr(self, 'custo_desde_o_inicio_cacheado_sem_recalculo'):
            return self.custo_desde_o_inicio_cacheado_sem_recalculo

        custo_acumulado = self.calcula_custo_de_transicao()
        if self.origem is not None:
            custo_acumulado += self.origem.calcula_custo_desde_o_inicio()
        self.custo_desde_o_inicio_cacheado_sem_recalculo = custo_acumulado
        return custo_acumulado

    def calcula_heuristica(self) -> int:
        pass

    def gera_movimentos_possiveis_deste(self) -> list:
        pass

    def busca_em_profundidade_iterativa(self) -> tuple:
        pilha_tabuleiros_a_expandir = [self]

        visitados = {}

        LIMITE_PROFUNDIDADE = 10

        limitado = LIMITE_PROFUNDIDADE

        while pilha_tabuleiros_a_expandir:
            while limitado > 0 and pilha_tabuleiros_a_expandir:
                tabuleiro_base = pilha_tabuleiros_a_expandir.pop()

                if not visitados.get(str(tabuleiro_base)) is None:
                    continue

                if tabuleiro_base.eh_estado_final():
                    return (tabuleiro_base, True)

                visitados[str(tabuleiro_base)] = tabuleiro_base

                pilha_tabuleiros_a_expandir += tabuleiro_base.gera_movimentos_possiveis_deste()
                limitado -= 1

            limitado = LIMITE_PROFUNDIDADE
            copia_pilha = list(pilha_tabuleiros_a_expandir)

            while copia_pilha:
                tabuleiro_base = copia_pilha.pop(0)

                if not visitados.get(str(tabuleiro_base)) is None:
                    continue

                if tabuleiro_base.eh_estado_final():
                    return (tabuleiro_base, True)

                visitados[str(tabuleiro_base)] = tabuleiro_base

                pilha_tabuleiros_a_expandir += tabuleiro_base.gera_movimentos_possiveis_deste()

        return (self, False)

    def busca_em_largura(self) -> tuple:
        estados_a_expandir = [self]
        visitados = {}

        while estados_a_expandir:
            estado: Estado = estados_a_expandir.pop(0)

            visitados[str(estado)] = estado

            if estado.eh_estado_final():
                return (estado, True)

            for proximo_a_inserir in estado.gera_movimentos_possiveis_deste():
                if visitados.get(str(proximo_a_inserir)) is None:
                    estados_a_expandir.append(proximo_a_inserir)

        return (None, False)

    def busca_de_custo_uniforme(self) -> tuple:
        estados_a_expandir = [self]
        visitados = {}
        
        custos_minimos = ([], False)

        while estados_a_expandir:
            estado: Estado = estados_a_expandir.pop(0)

            visitados[str(estado)] = estado
            
            if len(custos_minimos[0]) > 0 and estado.calcula_custo_desde_o_inicio() > custos_minimos[0][0].calcula_custo_desde_o_inicio():
                continue # consideracao lista esta ordenada

            if estado.eh_estado_final():
                custos_minimos[0].append(estado)
                custos_minimos[0].sort(key=lambda estado_na_fila: estado_na_fila.calcula_custo_desde_o_inicio())
                custos_minimos = (custos_minimos[0], True)

            for proximo_a_inserir in estado.gera_movimentos_possiveis_deste():
                if visitados.get(str(proximo_a_inserir)) is None:
                    estados_a_expandir.append(proximo_a_inserir)
            
            estados_a_expandir.sort(key=lambda estado_na_fila: estado_na_fila.calcula_custo_desde_o_inicio())

        return custos_minimos


    def subida_de_encosta(self, contador_repeticoes_custo=0) -> tuple:
        if self.eh_estado_final():
            return (self, True)

        movimentos_possiveis = self.gera_movimentos_possiveis_deste()

        menor_estado = self
        for movimento in movimentos_possiveis:
            if movimento.avalia_custo_do_estado_atual() <= menor_estado.avalia_custo_do_estado_atual():
                menor_estado = movimento

        if menor_estado.avalia_custo_do_estado_atual() < self.avalia_custo_do_estado_atual():
            menor_estado.limite_repeticoes_subida_de_encosta = self.limite_repeticoes_subida_de_encosta
            return menor_estado.subida_de_encosta()

        if menor_estado == self or contador_repeticoes_custo > self.limite_repeticoes_subida_de_encosta:
            return (self, False)
        
        return menor_estado.subida_de_encosta(contador_repeticoes_custo + 1)

    def subida_de_encosta_com_reinicio_aleatorio(self) -> tuple:
        visitados = {
            str(self): self
        }

        ultimo_menor_estado = self
        threshold = 2# self.limite_repeticoes_subida_de_encosta
        while True:
            menor_estado = ultimo_menor_estado
            if menor_estado.eh_estado_final():
                return (self, True)

            for movimento in self.gera_movimentos_possiveis_deste():
                visitados[str(movimento)] = movimento
                if movimento.avalia_custo_do_estado_atual() <= menor_estado.avalia_custo_do_estado_atual():
                    menor_estado = movimento

            if menor_estado.avalia_custo_do_estado_atual() < ultimo_menor_estado.avalia_custo_do_estado_atual():
                ultimo_menor_estado = menor_estado
            elif menor_estado.avalia_custo_do_estado_atual() == ultimo_menor_estado.avalia_custo_do_estado_atual() and threshold > 0 and menor_estado != ultimo_menor_estado:
                ultimo_menor_estado = menor_estado
                threshold -= 1
            else:
                threshold = 2# self.limite_repeticoes_subida_de_encosta
                visitado_randomico = choice(list(visitados.values()))
                ultimo_menor_estado = choice(visitado_randomico.gera_movimentos_possiveis_deste())
                


    def criar_caminho_string(self):
        caminho_ate_ele = "--- INICIO ---\n"

        if self.origem is not None:
            caminho_ate_ele = self.origem.criar_caminho_string()
            
        return caminho_ate_ele + str(self) + "\n\n"

    def __str__(self):
        return str(self.tabuleiro)