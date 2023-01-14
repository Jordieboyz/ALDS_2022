# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 23:56:55 2023

@author: boerj
"""

# get all the adjacent move in offset direction from a position ont he board
def get_adj_moves(state, move, player=0, offset=3):
    # pre alloc max amount of moves out of this function? is kinda annoying because we dont use a simple assigning value
    new_moveset = []
    
    # create matrix of offset
    for i in range(-offset, offset+1, 1):
        if i != 0:
            directions = [(i, i), (i, i*-1), (i, 0), (0, i)]
            
            # always 4, constant TimeComplexity
            for _dir in directions:
                
                # translate to real coord
                tMove = addTuple(_dir, move)
                # validate
                if isValidMoveOnBoard(state[0], tMove[0], tMove[1], player):
                    # add if nog already in
                    new_moveset.append(tMove)
    return new_moveset





def addTuple(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))
.


def translate_to_coord(coord, matrix):
    return [addTuple(coord, c) for c in matrix]
    
def adj_by_4_matrix(state, coordinate):
    return translate_to_coord(coordinate, getMatrix(3))

def get_adjacent_moves(state, coordinate, player=0):
    return validate_moves(state, adj_by_4_matrix(state, coordinate), player)
    
def validate_moves(state, moves, player=0):
    return list(filter(None, map(lambda x: x if isValidMoveOnBoard(state[0], x[0], x[1], player) else None, moves)))

def remove_duplicates(oList):
    return [*set(oList)]


def isValidMoveOnBoard(board, row, col, player=0):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    
    debug = False
    if debug:
        print(board)
        
        print((row >= 0))
        print((col >= 0))
        print((col < len(board[0])))
        print((board[row][col] == 0))
    return (
        (row >= 0)
        and (row < len(board))
        and (col >= 0)
        and (col < len(board[0]))
        and (board[row][col] == 0 or board[row][col] == player)
    )



def get_valid_moves(state, adj=False, player=None):
    # make sure we dot use the player if we dont use adj
    board = state[0]
    all_moves = []
    if not adj:
        player = 0
    else:
        if player == None:
            all_moves = list(zip(*np.where(board != 0)))
        else:
            all_moves = list(zip(*np.where(board == player)))
            
    if all_moves:
        if adj:
            moveset = []
            for move in all_moves:
                moveset.extend(get_adj_moves(state, move))
            return remove_duplicates(moveset)
        else:
            return all_moves 
    else:
        return []
    
    
    



# start = time.perf_counter_ns()
# l = []
# for i in range(0,32):
#     l.append((0, 0))
    
# end = time.perf_counter_ns()-start
# print('took: ', end) 


# start_2 = time.perf_counter_ns()
# l = [None]*32
# for i in range(0,32):
#     l[i] = (1, 1)
# end = time.perf_counter_ns()-start_2
# print('took: ', end) 
# state = np.zeros(shape=(19, 19), dtype=int), 1
# coord = (9, 9)

# state[0][9][9] = 2


# # print(static_matrix_3)



# start = time.perf_counter_ns()
# for i in range(0, 19):
#     get_adj_moves(state, coord)
# end_1 = time.perf_counter_ns()-start
# print('preMat took: ', end_1)


# start = time.perf_counter_ns()
# for i in range(0, 19):
#     get_adj_moves(state, coord)
# end_2 = time.perf_counter_ns()-start
# print('normal took: ', end_2)


# print('; difference: ', end_1-end_2)


# print(static_matrix_3)
# print('a==b: ', len(a)==len(b))



