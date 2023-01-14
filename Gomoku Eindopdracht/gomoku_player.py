import random
import copy
import math
import numpy as np
import time
# from gomoku import valid_moves
from GmUtils import GmUtils

class node:
    def __init__(self, state, parent, init_move):
        self.state = state
        self.parent = parent
        self.init_move = init_move
        self.valid_moves = []
        self.children = []
        self.N = 0
        self.Q = 0
    
    def printNode(self):
            print()
            print('parent: ', self.parent)
            print('init_move: ', self.init_move)
            print()       
            # pretty_board(self.state[0])
            
            for child in self.children:
                print('child: ', child.init_move, "N: ", child.N, "Q: ", child.Q, "  ->  ", (child.Q/child.N))

def get_valid_moves(state, get_opening=False): 
    def is_possible_move(move):
        if(move[0] >= 0)\
            and (move[0] < len(state[0]))\
            and (move[1] >= 0)\
            and (move[1] < len(state[0]))\
            and (state[0][move[0]][move[1]] == 0):
            return move
        else:
            return None
        
    board = state[0]
    ply = state[1]
    
    if get_opening:
        opening = star_points(((len(state[0]) // 2) // 2), len(state[0]), False)
        return list(filter(None, map(is_possible_move, opening)))
    else:
        if ply == 1:
            middle = np.array(np.shape(board)) // 2
            return [tuple(middle)]
        else:
            return list(zip(*np.where(board == 0)))
    
    
class basePlayer:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_
        self.valid_moves = []

    def new_game(self, black_: bool):
        """ At the start of each new game you will be notified by the competition.
            this method has a boolean parameter that informs your agent whether you
            will play black or white.
        """
        self.black = black_
    
    def move(self, state, last_move, max_time_to_move = 2000):
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        
        # This to make sure the tests can be done. Set this to False if we are playing some kind of competition.
        check_tests = False
        if check_tests:
            self.valid_moves = get_valid_moves(state)
        else:
            if state[1] < 3:
                self.valid_moves = get_valid_moves(state, True) # double floor division to get the 25%th index of the board
                if state[1] == 1:
                    return get_valid_moves(state)[0]
            else:
                if not self.valid_moves:
                    self.valid_moves = get_valid_moves(state, False)
                else:
                    if last_move in self.valid_moves:
                        self.valid_moves.remove(last_move)
        
        n_root = node(state, None, last_move)
        n_root.valid_moves = self.valid_moves        

        start_time = time.time()
        while ((time.time() - start_time) * 1000) < max_time_to_move:  
            n_leaf = FindSpotToExpand(n_root)
            val = rollout(n_leaf)
            BackupValue(n_leaf, val)
        
        # n_root.printNode()
        move = best_uct_child(n_root).init_move
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
        n_child.valid_moves = get_valid_moves(n_child.state)
        
        _node.children.append(n_child)
        return n_child
    
    maxUct_child = best_uct_child(_node, True)
    return maxUct_child
        
        
# O(n), the more moves there are, the more the function grows in time    
def rollout(_node):
    
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


# offset can be an integer from 0 - (len // 2)
def star_points(offset, bsize, sides=True):
    if offset >= (bsize // 2):
        return []
    
    offset -= 1  # now we can use it for indexing
    half_bsize = bsize // 2
    outer_bsize = (bsize-1) - offset
    
    if sides:
        return [(offset, offset),       (offset, half_bsize),        (offset, outer_bsize),
                (half_bsize, offset),                                (half_bsize, outer_bsize),
                (outer_bsize, offset), (outer_bsize, half_bsize),  (outer_bsize, outer_bsize)]
    else:
        return [(offset, offset), (offset, outer_bsize),
                (outer_bsize, offset),  (outer_bsize, outer_bsize)]
    
    
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


def sumr(n, total = 0):
    if n == 0:
        return total
    return sumr(n-1, total+n)

# nodes = np.zeros(shape=(19, 19))
def check():
    state= np.zeros((19, 19))
    nodes = []
    a = 19*19
    start = time.perf_counter()
    
    for i in range(0, sumr(a)*(a)):
        nodes.append(node(state, None, None))
    
    end = time.perf_counter()-start 
    print('this took: ', end)

check()


# print(sumr(a)*(a))
