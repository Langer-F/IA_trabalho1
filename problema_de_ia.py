import numpy as np
from random import choice

LIMITE_SUBIDA_DE_ENCOSTA = 30

class Estado:
    def __init__(self, tabuleiro, origem=None, limite_repeticoes_subida_de_encosta=LIMITE_SUBIDA_DE_ENCOSTA, iteracao=1):
        self.tabuleiro = tabuleiro
        self.origem = origem
        self.limite_repeticoes_subida_de_encosta = limite_repeticoes_subida_de_encosta
        self.iteracao = iteracao

    def eh_estado_final(self) -> bool:
        pass

    def calcula_temperatura(self) -> float:
        if not hasattr(self, 'temperatura_cacheada'):
            self.temperatura_cacheada = np.exp(
                ((self.calcula_custo_desde_o_inicio() - 
                 self.avalia_custo_do_estado_atual()) / 
                 (self.calcula_custo_desde_o_inicio()+1)))
        return self.temperatura_cacheada

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


    def subida_de_encosta(self) -> tuple:
        visitados = {
            str(self): self
        }
        ultimo_menor_estado = self
        threshold = self.limite_repeticoes_subida_de_encosta
        while threshold > 0:
            menor_estado = ultimo_menor_estado
            if menor_estado.eh_estado_final():
                return (menor_estado, True)

            for movimento in menor_estado.gera_movimentos_possiveis_deste():
                if visitados.get(str(movimento)) is not None:
                    continue
                visitados[str(movimento)] = movimento
                if movimento.avalia_custo_do_estado_atual() <= menor_estado.avalia_custo_do_estado_atual():
                    menor_estado = movimento

            if menor_estado.avalia_custo_do_estado_atual() < ultimo_menor_estado.avalia_custo_do_estado_atual():
                threshold = self.limite_repeticoes_subida_de_encosta
                ultimo_menor_estado = menor_estado
            elif menor_estado.avalia_custo_do_estado_atual() == ultimo_menor_estado.avalia_custo_do_estado_atual() and threshold > 0 and menor_estado != ultimo_menor_estado:
                ultimo_menor_estado = menor_estado
                threshold -= 1
            else:
                return (self, False)
        return (self, False)

    def subida_de_encosta_com_reinicio_aleatorio(self) -> tuple:
        visitados = {
            str(self): self
        }

        ultimo_menor_estado = self
        threshold = self.limite_repeticoes_subida_de_encosta
        while True:
            menor_estado = ultimo_menor_estado
            if menor_estado.eh_estado_final():
                return (menor_estado, True)

            for movimento in self.gera_movimentos_possiveis_deste():
                if visitados.get(str(movimento)) is not None:
                    continue
                visitados[str(movimento)] = movimento
                if movimento.avalia_custo_do_estado_atual() <= menor_estado.avalia_custo_do_estado_atual():
                    menor_estado = movimento

            if menor_estado.avalia_custo_do_estado_atual() < ultimo_menor_estado.avalia_custo_do_estado_atual():
                ultimo_menor_estado = menor_estado
            elif menor_estado.avalia_custo_do_estado_atual() == ultimo_menor_estado.avalia_custo_do_estado_atual() and threshold > 0 and menor_estado != ultimo_menor_estado:
                ultimo_menor_estado = menor_estado
                threshold -= 1
            else:
                threshold = self.limite_repeticoes_subida_de_encosta
                visitado_randomico = choice(list(visitados.values()))
                ultimo_menor_estado = choice(visitado_randomico.gera_movimentos_possiveis_deste())
                
    def simulated_annealing(self) -> tuple:
        visitados = {
            str(self): self
        }
        temperaturas = [self]

        menor_estado = self
        iteracao = 1
        while True:
            if menor_estado.eh_estado_final():
                return (menor_estado, True)

            iteracao += 1

            for movimento in self.gera_movimentos_possiveis_deste():
                if visitados.get(str(movimento)) is not None:
                    continue 
                visitados[str(movimento)] = movimento
                movimento.iteracao = iteracao
                temperaturas.append(movimento)
            
            temperaturas.sort(key=lambda estado_probabilistico: estado_probabilistico.calcula_temperatura())
            menor_estado = temperaturas.pop(0)
            
    def busca_a_estrela(self):
        visitados = {}

        #se o estado atual é final, retorna ele
        if self.eh_estado_final():
            return self
        
        movimentos_possiveis = self.gera_movimentos_possiveis_deste()
        achou_estado_final = False
        #gerar todos os filhos do nó atual
        custo_final = 10000000000000000
        #loop enquanto houver elementos em "movimentos_possiveis"
        while movimentos_possiveis:
            flag_menor_estado = False
            menor = custo_final

            #remover de "movimentos_possiveis" e adicionar em visitados quem tem (custo_total_de_transicao + heuristica) > "custo_final" 
            for i in movimentos_possiveis:
                x = (i.calcula_heuristica())
                x = x + i.calcula_custo_desde_o_inicio()

                if x>=custo_final:
                    visitados[str(i)] = i
                    movimentos_possiveis.remove(i)
                    #aqui remove i de movimentos possiveis e adiciona em visitados"""
                    continue


                #pesquisar em movimentos_possiveis se alguem é estado final
                if i.eh_estado_final():
                    #se alguem for estado final, atualiza custo final caso custo_total_de_transição < custo_final
                    if i.calcula_custo_desde_o_inicio() < custo_final:
                        achou_estado_final = True
                        custo_final = i.calcula_custo_desde_o_inicio()
                        estado_final = i


                #pesquisar em "movimentos_possiveis" quem tem o menor valor de (custo_total_de_transicao + heuristica)
                if x < menor:
                    flag_menor_estado = True
                    menor_estado = i
                    menor = x

            #gerar os filhos do menor de todos
            novos_estados =  menor_estado.gera_movimentos_possiveis_deste()
            
            for j in novos_estados:
                if str(j) not in visitados:
                    movimentos_possiveis.append(j)
            if flag_menor_estado:
                movimentos_possiveis.remove(menor_estado)
                visitados[str(menor_estado)] = menor_estado
                #remover menor_estado de "movimentos_possiveis" e adicionar em "visitados"
        return (estado_final,achou_estado_final)


    def criar_caminho_string(self):
        caminho_ate_ele = "--- INICIO ---\n"

        if self.origem is not None:
            caminho_ate_ele = self.origem.criar_caminho_string()
            
        return caminho_ate_ele + str(self) + "\n\n"

    def __str__(self):
        return str(self.tabuleiro)