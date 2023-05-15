from Rainha import Tabuleiro
import numpy as np
import matplotlib
import time


def test_tabuleiro_tamanho_fixo(tabuleiro):
    n = len(tabuleiro.tabuleiro)
    print()
    print(f"-----------------------TAMANHO {n}----------------------------")

    #teste A*
    time_start = time.time()
    teste = tabuleiro.busca_a_estrela()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Busca A* \t\t\t\t: {:.2f} segundos".format(tempo))
    
    #teste simullate annealing
    #time_start = time.time()
    #teste = tabuleiro.simulated_annealing()
    #tempo = time.time() - time_start
    #if teste[1] == True:
    #    print("Simullated annealing \t\t\t: {:.2f} segundos".format(tempo))
    
    #teste busca em profundidade iterativa
    time_start = time.time()
    teste = tabuleiro.busca_em_profundidade_iterativa()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Busca em profundidade \t\t\t: {:.2f} segundos".format(tempo))
    
    #teste busca em largura
    time_start = time.time()
    teste = tabuleiro.busca_em_largura()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Busca em largura \t\t\t: {:.2f} segundos".format(tempo))

    #teste busca de custo uniforme
    time_start = time.time()
    teste = tabuleiro.busca_de_custo_uniforme()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Busca de custo uniforme \t\t: {:.2f} segundos".format(tempo))

    #teste subida de encosta
    time_start = time.time()
    teste = tabuleiro.subida_de_encosta()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Subida de encosta \t\t\t: {:.2f} segundos".format(tempo))

    #teste subida de encosta com reinicio aleatorio
    time_start = time.time()
    teste = tabuleiro.subida_de_encosta_com_reinicio_aleatorio()
    tempo = time.time() - time_start
    if teste[1] == True:
        print("Subida de encosta, reinicio aleatorio \t: {:.2f} segundos".format(tempo))






def main():
    tabuleiro4 = Tabuleiro(np.array([
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 1, 0]
        ]))
    tabuleiro5 = Tabuleiro(np.array([
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ]))
    tabuleiro6 = Tabuleiro(np.array([
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0]
        ]))
    test_tabuleiro_tamanho_fixo(tabuleiro4)
    test_tabuleiro_tamanho_fixo(tabuleiro5)
    test_tabuleiro_tamanho_fixo(tabuleiro6)
    
    
if __name__ == '__main__':
    main()