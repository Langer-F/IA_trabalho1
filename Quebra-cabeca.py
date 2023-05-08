
def generate_boards():
    n = int(input("Digite o valor de N:"))
    board1 = ['B'] * n + ['0'] + ['P'] * n
    board2 = ['P'] * n + ['0'] + ['B'] * n
    return (tuple(board1), tuple(board2))

b1,b2 = generate_boards()
print(b1)
print(b2)





def generate_children(state):
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
                    new_state[empty_pos-1], new_state[empty_pos] = new_state[empty_pos], new_state[empty_pos-1]
                    cost = dist
                    children.append((tuple(new_state), cost))
                else:
                    new_state = list(state)
                    new_state[empty_pos+1], new_state[empty_pos] = new_state[empty_pos], new_state[empty_pos+1]
                    cost = dist
                    children.append((tuple(new_state), cost))
    return children


def is_goal(state): #verifica se é um estado final
    n = len(state) // 2
    
    # Verifica se a posição vazia está à esquerda ou à direita
    if state.index('0') < n:
        whites = state[:n]
        blacks = state[n+1:]
    else:
        whites = state[1:n+1]
        blacks = state[n:]
    
    # Verifica se todas as fichas brancas estão no meio das pretas
    for i, w in enumerate(whites):
        if w == 'B':
            for j, b in enumerate(blacks[:i]):
                if b == 'P':
                    return False
            for j, b in enumerate(blacks[i+1:]):
                if b == 'P':
                    return False
        elif w == '0':
            if 'B' in whites[i+1:] or 'B' in blacks:
                return False
        else:
            continue
    
    # Verifica se todas as fichas pretas estão no meio das brancas
    for i, b in enumerate(blacks):
        if b == 'P':
            for j, w in enumerate(whites[:i]):
                if w == 'B':
                    return False
            for j, w in enumerate(whites[i+1:]):
                if w == 'B':
                    return False
        elif b == '0':
            if 'P' in blacks[i+1:] or 'P' in whites:
                return False
        else:
            continue
    
    return True







