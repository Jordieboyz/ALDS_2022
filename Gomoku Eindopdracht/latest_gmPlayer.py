import random
import copy
import math
import numpy as np
import time
from gomoku import valid_moves, pretty_board
from GmUtils import GmUtils

class node:
    def __init__(self, state, parent, init_move):
        self.state = state
        self.parent = parent
        self.init_move = init_move
        self.valid_moves = []
        self.children = []
        self.fin = GmUtils.isWinningMove(init_move, state[0])
        self.N = 0
        self.Q = 0

class Utils:
    @staticmethod
    def getMatrix(offset):
        matrix = []
        for i in range(-offset, offset+1, 1):
            if i != 0:
                matrix.append((i, i))
                matrix.append((i, i*-1))
                matrix.append((i, 0))
                matrix.append((0, i))
        return matrix
    
    @staticmethod
    def multTuple(t1, t2):
        return tuple(map(lambda x, y: x * y, t1, t2))

    @staticmethod
    def addTuple(t1, t2):
        return tuple(map(lambda x, y: x + y, t1, t2))
    
    @staticmethod    
    def validate_moves(state, moves, player=0):
        return list(filter(None, map(lambda x: x if Utils.isValidMoveOnBoard(state[0], x[0], x[1], player) else None, moves)))
    
    @staticmethod
    def remove_duplicates(oList):
        return [*set(oList)]

    @staticmethod
    def isValidMoveOnBoard(board, row, col, player=0):
        # Returns True if there is an empty space in the given column.
        # Otherwise returns False.
        return (
            (row >= 0)
            and (row < len(board))
            and (col >= 0)
            and (col < len(board[0]))
            and (board[row][col] == 0 or board[row][col] == player)
        )



STATIC_MATRIXES = [Utils.getMatrix(i) for i in range(1, 6)]

# O(n)
# We loop through all the STATIC_MATRIX[offset] elements once and check if they are
# ... valid on the given state. We add these to a list (which is also O(n)) en return 
# ... the list of adjacent moves based on the given move and matrix. 
def get_adj_moves(state, move, offset):
    global STATIC_MATRIXES
    
    # Pre-allocation this list is possible, but in Python not worth the readability and compute time.
    # The time-difference between this and pre-allocation is negligible in this scenario.
    new_moveset = []
    
    # Always loops over a set amount of adjacent moves; len(static_matrix[offset])
    for m in STATIC_MATRIXES[offset-1]:

        # Translate matrix 'direction' to a on-board coordinate
        tMove = Utils.addTuple(m, move)
        
        # Check if this Translated coordinate is even valid
        if Utils.isValidMoveOnBoard(state[0], tMove[0], tMove[1]):
            new_moveset.append(tMove)
    return new_moveset



# O(1)
# We loop through a constant amount of 'directions' in the STATIC_MATRIX[0] aka 8. 
def get_max_sequence(state, move):
    global STATIC_MATRIXES
     

    board = state[0]
    who = board[move[0]][move[1]]
    max_seq = 1, (0, 0)
    working_on = False
    adj = 1 
    total = 1
    print(len(STATIC_MATRIXES[0]))
    
    # We always loop over 8 matrix 'directions'.
    for m in STATIC_MATRIXES[0]:
  
        adj = 1
        total = 1
        tMove = Utils.addTuple(m, move)
      
        if Utils.isValidMoveOnBoard(board, tMove[0], tMove[1], who):
 
            # if it is my won stone in dirirection m
            if board[tMove[0]][tMove[1]] == who:
                
                # start w 1 for the initial stone/move
                adj += 1
                
                working_on = True
                
                # We always do this maximum 3 times or less, but there is no input in play here
                for i in range(3):
        
                    tMove = Utils.addTuple(m, tMove)
                        
                        
                    # is valid is 0 or myself for sequence adding
                    if Utils.isValidMoveOnBoard(board, tMove[0], tMove[1], who):
                        
                        # if it is my won stone in dirirection m
                        if board[tMove[0]][tMove[1]] == who:
                            
                            if working_on:
                                adj += 1
                            else:
                                total += 1
                        
                        else:
                            if board[tMove[0]][tMove[1]] == 0:
                                
                                if working_on:
                                    if adj > max_seq[0]:
                                        # add initial move
                                        max_seq = adj, m
                                        
                                    total = adj
                                    working_on = False                
                    # it is the opponent
                    else:
                        working_on = False
                        break
                
                max_seq = total, Utils.addTuple(move, Utils.multTuple((adj,adj), m)) 
    return max_seq




# O(n)

def get_valid_moves(state, adj=False, adj_offset=1, player=None):
    # make sure we dot use the player if we dont use adj
    board = state[0]
    if state[1] == 1:
        return (len(board[0])//2, len(board[0])//2)
    else:
        if not adj or not player:
            return list(zip(*np.where(board == 0)))
        else:
            if player is None:
                player = 0
                
            all_player_moves = list(zip(*np.where(board == player)))
            
            if all_player_moves:
                moveset = []
                for move in all_player_moves:
                    moveset.extend(get_adj_moves(state, move, adj_offset))
                return Utils.remove_duplicates(moveset)
            return all_player_moves

# O(n)
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
                
    return Utils.remove_duplicates(Utils.validate_moves(state, threats))    
    
# O(1)    
# offset can be an integer from 0 - (len // 2)
def opening_star_points(offset, bsize):
    if offset >= (bsize // 2):
        return []
    
    offset -= 1  # now we can use it for indexing
    outer_bsize = (bsize-1) - offset
    
    return [(offset, offset), (offset, outer_bsize),
            (outer_bsize, offset),  (outer_bsize, outer_bsize)]

class basePlayer:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_


    def new_game(self, black_: bool):
        """ At the start of each new game you will be notified by the competition.
            this method has a boolean parameter that informs your agent whether you
            will play black or white.
        """
        self.black = black_
        # on startig a new game, create a list of opening moves
        self.valid_moves = opening_star_points(6, bsize=19)
        # self.valid_moves = []
        self.opening_done = False
        
        
        
    def move(self, state, last_move, max_time_to_move = 1000):
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        

        Tests = False
        if Tests:
            me = 2 if self.black else 1
            self.opening_done = True
            self.valid_moves =  get_valid_moves(state)
        else:
            me = 2 if self.black else 1
            if state[1] == 1:
                return get_valid_moves(state)
    
            if not self.valid_moves: 
                
                if not self.opening_done:
                    self.opening_done = True
                
                    self.valid_moves = get_valid_moves(state, True, 2, me)
            else:
                
                if last_move in self.valid_moves:
                    self.valid_moves.remove(last_move)
                
                if self.opening_done or not self.valid_moves:
                    if not self.opening_done:
                        self.opening_done = True
                    self.valid_moves = get_valid_moves(state, True, 2, me)
        
        # Tests focus more on attacking and winning in stead of defending first
        if Tests:
            if self.opening_done:
                attack = best_sequence_moves(state, me, 2)
                if attack:
                    self.valid_moves = attack
                else:
                    enemy = 1 if self.black else 2
                    defence = best_sequence_moves(state, enemy, 3)
                    if defence:
                        self.valid_moves = defence
                    else:
                        self.valid_moves = get_valid_moves(state, True, 2, me)
        else:
            if self.opening_done:
                enemy = 1 if self.black else 2
                defence = best_sequence_moves(state, enemy, 3)
                if defence:
                    self.valid_moves = defence
                else:
                    attack = best_sequence_moves(state, me, 2)
                    if attack:
                        self.valid_moves = attack
                    else:
                        self.valid_moves = get_valid_moves(state, True, 2, me)
            

        n_root = node(state, None, last_move)
        n_root.valid_moves = self.valid_moves        
        
        start_time = time.time()
        while ((time.time() - start_time) * 1000) < max_time_to_move:  
            n_leaf = FindSpotToExpand(n_root)
            val = rollout(n_leaf)
            BackupValue(n_leaf, val)

        move = best_uct_child(n_root).init_move

        if move in self.valid_moves:        
            self.valid_moves.remove(move)
        return move
    
    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Jort de Boer (1764801)"

# O(1), we always only backpropagate 2 nodes in the tree.
def BackupValue(_node, val):
    me_as_black = (_node.state[1]-1) % 2 == 1 # get back on the tree to figure out who I am
    while _node is not None:
        _node.N += 1
        if (me_as_black and _node.state[1] % 2 == 1) or \
                (not me_as_black and _node.state[1] % 2 == 0):
            _node.Q = _node.Q - val
        else:
            _node.Q = _node.Q + val
            
        me_as_black = not me_as_black
        _node = _node.parent
        
# O(n), loop once over all the children        
def best_uct_child(_node, upper_confidence_bound = False):
    # problem with a lookuptable
    # floats arnt integers
    # we need the boundaries for the n.Q and n.N check, that is not worth it
    # we need as much time we need in the early stages of the game, later, we have less moves, so more accurate, 
    # but realy, we have a lot of choices mo, so we kinda waste comp time
    # O(1)
    def uct(n):
        if upper_confidence_bound:
            return (n.Q/n.N) + (2 * math.sqrt( (math.log(n.parent.N) / n.N)))
        return (n.Q/n.N)
    
    
    if _node.children:
        best_child = (0, 0)
        for i, child in enumerate(_node.children):
            if child.fin:
                return child
            uct_val = uct(child)
            if uct_val > best_child[1]:
                best_child = (i, uct_val)
        return _node.children[best_child[0]]
    return None


# O(n), it is either the timeComplexity of the best_uct_child or we need to get, create and add a new node, 
# ... wich always depens on the len and in the worst case is is the same as the input_len
def FindSpotToExpand(_node):
    if not _node.valid_moves:
        return _node
     
    if len(_node.children) != len(_node.valid_moves):
        init_move_child = _node.valid_moves[len(_node.children)]
       
        n_child = node(new_game_state(_node.state, init_move_child), 
                       _node, 
                       init_move_child)
        
        # copy is possible just because we dont need to save the moves for the children
        # ... we kinda remove them after ever rollout.
        n_child.valid_moves = get_valid_moves(n_child.state, True, 4)
        # n_child.valid_moves.remove(init_move_child)
        

        _node.children.append(n_child)
        return n_child
    
    maxUct_child = best_uct_child(_node, True)
    return maxUct_child
        
        
# O(n), the more moves there are, the more the function grows in time    
def rollout(_node):
    if _node.fin:
        return 1
    
    sim_state = _node.state
    last_move = _node.init_move
    sim_moves = copy.copy(_node.valid_moves)
    who = _node.state[1] % 2 

    # stop when somebody wins, otherwise, simulate until there are no moves left to simulate
    while not GmUtils.isWinningMove(last_move, sim_state[0]):
        # draw, no Win and no moves
        if not sim_moves:
            return 0.5
        
        who = not who
        
        last_move = random.choice(sim_moves)
        sim_state = new_game_state(sim_state, last_move)
        sim_moves.remove(last_move)

    
    if who == _node.state[1] % 2:
        return 1
    else:
        return 0

# O(1), There is nothing special in this function tbh
def new_game_state(state, move):
    # It is possible to use the copy.deepcopy(), but this function in incredibly slow, so for every rolloutstate
    # ... we rather use this, so we have more time for the rest of the rollout and maybe exploring more children
    new_game_state = np.array(state[0]), state[1] + 1
    if new_game_state[0][move[0]][move[1]] == 0:
        new_game_state[0][move[0]][move[1]] = 1 if state[1] % 2 == 0 else 2
    else:
        return None
    return new_game_state 


state = np.zeros((19, 19), dtype=int), 0
board = state[0]
middle = (len(board[0])//2, len(board[0])//2)
state = new_game_state(state, middle) #1
state = new_game_state(state, (0, 0)) #2

state = new_game_state(state, (16, 18)) #3
state = new_game_state(state, (2, 2)) #4

state = new_game_state(state, (16, 17)) #6
state = new_game_state(state, (7, 7)) #5

state = new_game_state(state, (15, 18)) #6
state = new_game_state(state, (11, 8)) #5

state = new_game_state(state, (16, 15)) #6
state = new_game_state(state, (7, 4)) #5

state = new_game_state(state, (13, 18)) #6
state = new_game_state(state, (7, 9)) #5


pretty_board(state[0])
# me = 1 if self.black else 2
moves = list(zip(*np.where(state[0] == 1)))
for move in moves:
    seq = get_max_sequence(state, move)
    # if seq >= 3:
    print('threat for: ', move, ' w: ', seq)


# threat for:  (9, 9)  w:  (1, (0, 0))
# threat for:  (13, 18)  w:  (1, (0, 0))
# threat for:  (15, 18)  w:  (2, (17, 18))
# threat for:  (16, 15)  w:  (1, (0, 0))
# threat for:  (16, 17)  w:  (1, (16, 19))
# threat for:  (16, 18)  w:  (3, (16, 16))