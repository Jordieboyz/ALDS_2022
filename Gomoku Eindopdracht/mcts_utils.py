import random
import copy
import math
import numpy as np
from gmAIgent import get_valid_moves
from gomoku import check_win

# Class: node
# This class is the main class for creating our 'tree'.
# node doesn't have any functions, we just save data so we can refer to it when walking through the 'tree'
class node:
    def __init__(self, state, parent, init_move):
        self.state = state
        self.parent = parent
        self.init_move = init_move
        self.valid_moves = []
        self.children = []
        self.fin = check_win(state[0], init_move)
        self.N = 0
        self.Q = 0
        

# O(n), it is either the timeComplexity of the best_uct_child or we need to get, create and add a new node, 
# ... wich always depens on the len and in the worst case is is the same as the input_len, so O(n)
def FindSpotToExpand(_node):
    if not _node.valid_moves:
        return _node
     
    if len(_node.children) != len(_node.valid_moves):
        init_move_child = _node.valid_moves[len(_node.children)]
       
        n_child = node(new_game_state(_node.state, init_move_child), 
                       _node, 
                       init_move_child)
        
        # we get all the possible moves, so we van actually playthe whole game until we get a final state
        # Due to the specific move selection from every node, we can't just copy the moves from the _node
        n_child.valid_moves = get_valid_moves(n_child.state)
        
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
    while not check_win(sim_state[0], last_move):
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
    # I tried implementing a lookupTable for the UCT-values.
    # This wasn't really worth it..
    # We need to deal with a way of using floats (x.5 values) as integers (this is possivle, but not worth the compute time)
    # We need to set boundaries for either the array where we store the values or we need to set a 'roof' for both.

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




