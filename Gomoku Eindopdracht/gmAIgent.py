import numpy as np

# Class: Utils
# A class which defines some standard much needed functions which improve readability
class gmAgent_Utils:
    # O(offset*2)
    # Get a Square-Matrix with an width and length of offset
    # example: getMatrix(2) -> [(-2, -2)          (-2, 0)         (-2, 2)
    #                                    (-1, -1) (-1, 0) (-1, 1)
    #                           (0,  -2) (0,  -1)         (0,  1) (0,  2)             
    #                                    (1,  -1) (1,  0) (1,  1)
    #                           (2,  -2)          (2,  0)         (2,  2)]
    def getMatrix(offset):
        matrix = []
        for i in range(-offset, offset+1, 1):
            if i != 0:
                matrix.append((i, i))
                matrix.append((i, i*-1))
                matrix.append((i, 0))
                matrix.append((0, i))
        return matrix
    
    
    # O(1)
    # Multiple two Tuples
    # example:  multTuple((3, 4), (-1, -1)) -> (-3, -4)
    def multTuple(t1, t2):
        return tuple(map(lambda x, y: x * y, t1, t2))
    
    
    # O(1)
    # Add two Tuples
    # example:  addTuple((3, 4), (-1, -1)) -> (2, 3)
    def addTuple(t1, t2):
        return tuple(map(lambda x, y: x + y, t1, t2))
    
    
    # O(n)
    # Check for all the moves in a list if they are valid in a given state.
    # We can also check if moves are from a specific player  
    def validate_moves(state, moves, player=0):
        return list(filter(None, map(lambda x: x if gmAgent_Utils.isValidMoveOnBoard(state[0], x[0], x[1], player) else None, moves)))
    
    
    # O(n)
    # Remove duplicates out of a list
    def remove_duplicates(oList):
        return [*set(oList)]
    
    
    # O(1)
    # Check wether the given move is valid onthe given state
    def isValidMoveOnBoard(board, row, col, player=0):
        return ((row >= 0) and (row < len(board))
            and (col >= 0) and (col < len(board[0]))
            and (board[row][col] == 0 or board[row][col] == player))


# These are Matrixes and the content will be referred to as 'directions'
# ... although these are not really just directions, the Tuples in here are a combination of the offset and the direction
STATIC_MATRIXES = [gmAgent_Utils.getMatrix(i) for i in range(1, 6)]


# O(n)
# We loop through all the directions once and check if they are
# ... valid on the given state. We add these to a list and return 
# ... the list of adjacent moves based on the given move and matrix. 
def get_adj_moves(state, move, offset):
    global STATIC_MATRIXES
    
    # Pre-allocation this list is possible, but in Python not worth the readability and compute time.
    # The time-difference between this and pre-allocation is negligible in this scenario.
    new_moveset = []
    
    # Loop over all the 'directions'
    for m in STATIC_MATRIXES[offset-1]:

        # Translate 'direction' to a on-board coordinate
        tMove = gmAgent_Utils.addTuple(m, move)
        
        # Check if this Translated coordinate is even valid
        if gmAgent_Utils.isValidMoveOnBoard(state[0], tMove[0], tMove[1]):
            new_moveset.append(tMove)
    return new_moveset


# O(n), there are a couple of functions who use O(n), becasue we generally use a way of getting all moves on a board.
# This function returns a list of valid moves based on the parameters of the function.
def get_valid_moves(state, adj=False, adj_offset=1, player=None):
    board = state[0]
    # Return middle if its the initial state of the game
    if state[1] == 1:
        return [(len(board[0])//2, len(board[0])//2)]
    else:
        # Return ALL possible moves on the board
        if not adj or not player:
            return list(zip(*np.where(board == 0)))
        else:
            if player is None:
                player = 0
            
            # get all adjacent moves based on 'player'
            all_player_moves = list(zip(*np.where(board == player)))
            
            if all_player_moves:
                moveset = []
                for move in all_player_moves:
                    moveset.extend(get_adj_moves(state, move, adj_offset))
                return gmAgent_Utils.remove_duplicates(moveset)
            return all_player_moves


# O(1), We loop through a constant amount of 'directions' in the STATIC_MATRIX[0] aka 8. 
# This function return a Tuple of the total amount of stones in any direction as a indicator of a threat and
# ... it return a move on the end of a found sequence. (this can be used to either stop an enemy sequence or continue your own)
def get_max_sequence(state, move):
    global STATIC_MATRIXES

    board = state[0]
    who = board[move[0]][move[1]]
    
    max_seq = 1, (0, 0)
    working_on_seq = False

    for m in STATIC_MATRIXES[0]:
        
        # set the standard to 1, so we count from the center (we assume this is a valid move)
        adj = 1
        total = 1
        
        # Translate the move to direction m
        tMove = gmAgent_Utils.addTuple(m, move)
      
        # Check wether my first move is valid and the stone of the player whomst this function 
        # is called upon 
        if gmAgent_Utils.isValidMoveOnBoard(board, tMove[0], tMove[1], who) and \
            board[tMove[0]][tMove[1]] == who:
                
                adj += 1
                
                working_on_seq = True
                
                # We always do this maximum 3 times or less, but there is no input in play here
                for i in range(3):
        
                    tMove = gmAgent_Utils.addTuple(m, tMove)
                    
                    # The Tmove is one of the player whomst this function is called upon
                    if gmAgent_Utils.isValidMoveOnBoard(board, tMove[0], tMove[1], who):
                        if board[tMove[0]][tMove[1]] == who:
                            if working_on_seq:
                                adj += 1
                            else:
                                total += 1
                        else:
                            if working_on_seq:
                                if adj > max_seq[0]:
                                    max_seq = adj, m
                                    
                                total = adj
                                working_on_seq = False                
                    # it is the opponent
                    else:
                        working_on_seq = False
                        break
                
                max_seq = total, gmAgent_Utils.addTuple(move, gmAgent_Utils.multTuple((adj,adj), m)) 
    return max_seq


# O(n), we loop throught the whole board to get all the moves of 'player'
# Return a list of 'threats'. This means, we check the sequences of all move in all directions
# ... and add moves based on mSeq. Threats of 4 are the highest priority, sonif there is one, we return it immediately
def best_sequence_moves(state, player, mSeq=3):
    
    moves = list(zip(*np.where(state[0] == player)))
    
    threats = []
    for move in moves:
        seq = get_max_sequence(state, move)
        if seq[0] >= mSeq:
            if seq[0] == 4:
                return [seq[1]]
            else:
                # all the seq of 3
                threats.append(seq[1])
                
    return gmAgent_Utils.remove_duplicates(gmAgent_Utils.validate_moves(state, threats))    
    

# O(1), There are no parameters which impact the runtime of this function.
# This function returns the same list every time.    
def opening_star_points(offset, bsize):
    if offset >= (bsize // 2):
        return []
    
    # now we can use it for indexing
    offset -= 1
    outer_bsize = (bsize-1) - offset
    
    return [(offset, offset), (offset, outer_bsize),
            (outer_bsize, offset),  (outer_bsize, outer_bsize)]
