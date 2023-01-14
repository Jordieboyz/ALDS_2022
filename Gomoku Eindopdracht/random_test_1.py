import random
import copy
import math
import numpy as np
import time
from gomoku import valid_moves
from GmUtils import GmUtils

C_CONST=2

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
            # if child.fin:
            #     print('This state is a direct winner!')
class random_test_player1:
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
        self.valid_moves = []
    
    def move(self, state, last_move, max_time_to_move = 1000):
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        
        # This to make sure the tests can be done. Set this to False if we are playing some kind of competition.
        check_tests = False
        if check_tests:
            self.valid_moves = valid_moves(state)
        else:
            if not self.valid_moves:
                if state[1] == 1:      # state[1] == 1
                    return valid_moves(state)[0]
                self.valid_moves = valid_moves(state)
            else:
                if last_move in self.valid_moves:
                    self.valid_moves.remove(last_move)
                
                if not self.valid_moves:
                    self.valid_moves = valid_moves(state)
                

        n_root = node(state, None, last_move)
        n_root.valid_moves = self.valid_moves        

        start_time = time.time()
        while ((time.time() - start_time) * 1000) < max_time_to_move:  
            n_leaf = FindSpotToExpand(n_root)
            val = rollout(n_leaf)
            BackupValue(n_leaf, val)
         
        move = best_uct_child(n_root).init_move
        self.valid_moves.remove(move)
        return move
    
    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Jort de Boer (1764801) -> C: " + str(C_CONST)

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
            return (n.Q/n.N) + (C_CONST * math.sqrt( (math.log(n.parent.N) / n.N)))
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
        # init_move_child = _node.valid_moves[len(_node.children)]
        init_move_child = random.choice(_node.valid_moves)
        
        
        n_child = node(new_game_state(_node.state, init_move_child), 
                       _node, 
                       init_move_child)
        
        n_child.valid_moves = valid_moves(n_child.state)
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