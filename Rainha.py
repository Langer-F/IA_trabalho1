import numpy as np


def calcula_custo(tabuleiro):
    """Dado um tabuleiro, calcula quantos pares de rainhas estão 'Se atacando'"""
    n = len(tabuleiro)
    custo = 0
    
    for i in range(n):
        for j in range(n):
            if tabuleiro[i][j]==1:
                for k in range(n):
                    if k != i:  #custo da linha
                        custo = custo + tabuleiro[k][j]
                    if k != j:  #custo da coluna
                        custo = custo + tabuleiro[i][k]
                    if k > 0:   #custo das diagonais
                        if (i+k) < n and (j+k) < n:
                            custo = custo + tabuleiro[i+k][j+k]
                        if (i+k) < n and (j-k) >=0:
                            custo = custo + tabuleiro[i+k][j-k]
                        if (i-k) >= 0 and (j+k) < n:
                            custo = custo + tabuleiro[i-k][j+k]
                        if (i-k) >= 0 and (j-k) >= 0:
                            custo = custo + tabuleiro[i-k][j-k]
    return custo//2                     

def troca_linha(tabuleiro,i1: int,i2: int):
    """Dado um tabuleiro e dois valores i1 e i2, troca as linhas i1 e i2 de lugar,
    ou seja, i1 vai para onde i2 estava e i2 vai para onde i1 estava"""
    aux = tabuleiro.copy()
    tabuleiro[i1] = tabuleiro[i2]
    tabuleiro[i2] = aux[i1]
    return tabuleiro

def troca_coluna(tabuleiro, j1: int, j2: int):
    """Dado um tabuleiro e dois valores j1 e j2, troca as linhas j1 e j2 de lugar,
    ou seja, j1 vai para onde j2 estava e j2 vai para onde j1 estava"""
    aux = tabuleiro.copy()
    tabuleiro[:,j1] = tabuleiro[:,j2]
    tabuleiro[:,j2] = aux[:,j1]
    return tabuleiro

def cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(n: int):
    """Cria um tabuleiro NxN com N rainhas posicionadas, sendo que nenhuma linha ou coluna repete"""
    tabuleiro = np.zeros((n,n),dtype=int)
    for i in range(n):
        linha_ja_ocupada = True
        while linha_ja_ocupada:
            coluna = np.random.randint(0,n)
            linha_ja_ocupada = False
            for j in range(n):
                if tabuleiro[j][coluna]==1:
                    linha_ja_ocupada = True
                    break
        tabuleiro[i][coluna] = 1
    return tabuleiro    
    
def cria_tabuleiro_inicial_aleatorio(n: int):
    """Cria um tabuleiro NxN com N rainhas posicionadas aleatoriamente, sem restrição (obviamente uma rainha nao pode ocupar uma casa já ocupada)"""
    tabuleiro = np.zeros((n,n),dtype = int)
    for _ in range(n):
        linha = np.random.randint(0,n)
        coluna = np.random.randint(0,n)
        while tabuleiro[linha][coluna] == 1:
            linha = np.random.randint(0,n)
            coluna = np.random.randint(0,n)
        tabuleiro[linha][coluna] = 1
    return tabuleiro




def main():
    tabuleiro = cria_tabuleiro_inicial_sem_linha_nem_coluna_repetida(15)
    #tabuleiro = cria_tabuleiro_inicial_aleatorio(6)
    print(tabuleiro)
    print(calcula_custo(tabuleiro= tabuleiro))
    #tabuleiro = troca_coluna(tabuleiro,0,1)
    #print("-------------------------------------------")
    #print(tabuleiro)




if __name__ == '__main__':
    main()

