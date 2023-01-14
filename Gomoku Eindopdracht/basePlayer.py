import random
import copy
import math
import numpy as np
import time
from gomoku import valid_moves
from GmUtils import GmUtils

class node:
    def __init__(self, state, parent, init_move):
        self.state = state
        self.parent = parent
        self.init_move = init_move
        self.valid_moves = []
        self.children = []
        self.fin = False if parent is None else GmUtils.isWinningMove(init_move, state[0])
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
                if child.fin:
                    print('This state is a direct winner!')

# implement opening + smart moves w matrix
# def get_smart_moves(state, opening=True)

# offset can be an integer from 0 - (len // 2)
# this only works w a size of 19 currently
def star_points(offset, bsize = 19, sides=False):
    if offset >= (bsize // 2):
        return []
    
    offset -= 1  # now we can use it for indexing
    # half_bsize = bsize // 2
    outer_bsize = (bsize-1) - offset
    
    # if sides:
    #     return [                       (offset, half_bsize),       
    #             (half_bsize, offset),                                (half_bsize, outer_bsize),
    #                                      (outer_bsize, half_bsize)]
    # else:
    return [(offset, offset), (offset, outer_bsize),
            (outer_bsize, offset),  (outer_bsize, outer_bsize)]
    

def addLists(l1, l2):
    if not l1:
        return l2
    l1.extend(l2)
    return l1
    
def addGenericType(type_, type_1, type_2):
    # prevent NoneType adding, wiil resuilt in errors
    if not type_1:
        return type_2
    if not type_2:
        return type_1
    
    return type_(map(lambda x, y: x + y, type_1, type_2))

# def addTuple(t1, t2):
#     return tuple(map(lambda x, y: x + y, t1, t2))

def translate(coord, coordlist):
    return [addGenericType(tuple, coord, c) for c in coordlist]
    
def getMatrix(offset, lDia=True, rDia=True, vert=True, hor=True):
    matrix = []
    for i in range(-offset, offset+1, 1):
        if i != 0:
            if lDia:
                matrix.append((i, i))
            if rDia:
                matrix.append((i, i*-1))
            if vert:
                matrix.append((i, 0))
            if hor:
                matrix.append((0, i))
    return matrix
    
def adj_by_4(state, coordinate, width=4, player=0, lDia=True, rDia=True, vert=True, hor=True):
    return validate_moves(state, translate(coordinate , getMatrix(4, lDia=True, rDia=True, vert=True, hor=True)), player)


def get_all_info(bsize):

    shape = (bsize, bsize)
    lookup = np.empty(shape, dtype=list) 
    board = (np.full(shape, 0), 0)

    for i in range(0, bsize, 1):
        for j in range(0, bsize, 1):
            lookup[i][j] = validate_moves(board, adj_by_4(board, (i, j)))

    return lookup    


def validate_moves(state, moves, player=0):
    return list(filter(None, map(lambda x: x if isValidMoveOnBoard(state[0], x[0], x[1], player) else None, moves)))

def remove_duplicates(oList):
    return [*set(oList)]

def isValidMoveOnBoard(board, row, col, player):
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
    
def get_smart_moves(state, just_opponent=False):
    if just_opponent:
        opponent = 1 if state[1] % 2 == 0 else 2
        used_moves = list(zip(*np.where(state[0] == opponent)))
    else:
        used_moves = list(zip(*np.where(state[0] != 0)))
    
    smart_moves = []        
    for move in used_moves:
        smart_moves	= addLists(smart_moves, adj_by_4(state, move))
    
    # dotn need to validate, bcs smart moves is made out oif validated adj_by_4 moves
    return  smart_moves

    
# def all_maxes(iterable):
#     maxes = []
#     val = 0
#     for i in iterable:
#         if i >= val:
            
    
    
    
    
def get_valid_moves(state, done_opening=False): 
    if state:
        board = state[0]
        ply = state[1]
        if ply == 1:
            middle = np.array(np.shape(board)) // 2
            return [], [tuple(middle)]

        moveset = []
        if not done_opening:
            starting_corners = star_points(5)
            if ply <= 5:
                moveset = starting_corners
            else:
                moveset = addLists(starting_corners, get_smart_moves(state, just_opponent=True))
        else:
            enemy_moves = []
            threats = check_threats(state)
            for a in threats:
                if max(a[1]) >= 3:

                    enemy_moves = remove_duplicates(addLists(enemy_moves, adj_by_4(state, a[0] )))
                    
            print('enemy moves: ', enemy_moves)
                    

            moveset = get_smart_moves(state)
            
        
        
        
        
        
        
        
        return remove_duplicates(validate_moves(state, moveset))
    else:
        print('is not a state')
        return None


def looping_through(start, direction, n):
    seq = 0
    for i in range(n):
        3
        if check_valid_and_opponent(start, direction, ):
            seq += 1
        else:
            return seq
                 
    
    

def check_threats(state, offset=4 ):
    def check_valid_and_opponent(move, offset, player):
        return (isValidMoveOnBoard(state[0], move[0]+offset[0], move[1]+offset[1], player)) \
                    and (state[0][move[0]+offset[0]][move[1]+offset[1]] == player)
    
    opponent = 1 if state[1] % 2 == 0 else 2
    used_moves = list(zip(*np.where(state[0] == opponent)))
    if used_moves:
        checked_moves = []
        for move in used_moves:
            # left_dia, right_dia, vert, hor
            sequences = [0, 0, 0, 0]
            tmp = [0, 0, 0, 0]
            
            for i in range(-offset, offset+1, 1):
                if check_valid_and_opponent(move, (i, i), opponent):
                    tmp[0] += 1
                else:
                    tmp[0] = 0
                    
                if check_valid_and_opponent(move, (i, i*-1), opponent):
                    tmp[1] += 1
                else:
                    tmp[1] = 0
                    
                if check_valid_and_opponent(move, (i, 0), opponent):
                    tmp[2] += 1
                else:
                    tmp[2] = 0
                    
                if check_valid_and_opponent(move, (0, i), opponent):
                    tmp[3] += 1
                else:
                    tmp[3] = 0
                    
                for i in range(len(tmp)):
                    if tmp[i] > sequences[i]:
                        sequences[i] = tmp[i]
                    
            checked_moves.append((move, sequences))
        return checked_moves
    else:
        return used_moves


# TODO: fix get_valid_moves
#   - check for enemy sequences. if more then 3, try and stop it. else choose an adjacent move of myself we random rollout
#   - immediately win if a child with winning move is poresent - DONE!
#   - full opening, just gotta figure out when we are done w the opening. 
#       - maybe have 2 seperate lists of enemy and my moves, where enemy is prioritized based on sequence
#       - and my moves are adjac ent from already placed moves? so we dont waste time going completely random
#
#   Defence is the best offence
#
#


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
        
        # reset for new games
        self.my_valid_moves = []
        self.enemy_valid_moves = []
        
        # make sure the first move possivble, the valid_+moves get filled
        self.dirty_flag = True
        
        self.done_corners = False 
        self.lookup_table = get_all_info(19)

    def move(self, state, last_move, max_time_to_move = 1000):
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        print(state[1])
        # This to make sure the tests can be done. Set this to False if we are playing some kind of competition.
        check_tests = True
        if check_tests:
            a = get_valid_moves(state, True)
            # print(a)
            self.valid_moves = valid_moves(state)
            # start = time.perf_counter_ns()
            # a = check_threats(state)
            # print()
            # print('took: ', time.perf_counter_ns()-start)
        
        else:
           
            # just the middle
            if state[1] == 1:
                return get_valid_moves(state, False)[0]
            
            # flag is set when one of the booleans changed
            # pretty much when list is empty, or done w sequence 
            # dirty flag, means, create new set (opening or sides or rest)
            # set when done corners is also True
            if self.dirty_flag:
                self.valid_moves = get_valid_moves(state, self.done_corners) # this is opening, so get the opening moves
                self.dirty_flag = False
                
            if self.done_corners:
                print('is true')
                if last_move in self.valid_moves:
                    print('in here')
                    self.valid_moves.remove(last_move)
                    self.valid_moves = addLists(self.valid_moves, adj_by_4(state, last_move))
                    remove_duplicates(validate_moves(state, self.valid_moves))
            # if self.dirty_flag:
            #     self.valid_moves = get_valid_moves(state, self.done_corners) # this is opening, so get the opening moves
            #     self.dirty_flag = False
           
            # first 2 moves are free of danger (3 and 5)

            
                # if last_move in self.valid_moves:
                #     self.valid_moves.remove(last_move)
                # self.valid_moves = addLists(self.valid_moves, adj_by_4(state, last_move))
                # remove_duplicates(self.valid_moves)
                    
                # if last_move in self.valid_moves:
                #     print('done this')
                # self.valid_moves = addLists(self.valid_moves, adj_by_4(state, last_move))


        n_root = node(state, None, last_move)
        n_root.valid_moves = self.valid_moves

        counter = 0
        start_time = time.time()
        while ((time.time() - start_time) * 1000) < max_time_to_move:  
            n_leaf = FindSpotToExpand(n_root, self.done_corners)
            val = rollout(n_leaf)
            BackupValue(n_leaf, val)
            counter += 1
        print('we did: ', counter, ' loops!')
        
        # n_root.printNode()
        


        move = best_uct_child(n_root).init_move
        
        # remove opposite move in opening, to prevent overcomplixcating the AI
        # TODO, side star tpoints remove the opposite
        if state[1] <= 5:                
            rMove = None
            if move[0] == move[1]:
                # eitehr 4, 4 or 14, 14
                if move[0] == 4:
                    rMove = (14, 14)
                else:
                    rMove = (4, 4)
            else:
                # 14, 4 -> 4, 14
                rMove = (move[1], move[0]) 
            
            if rMove and rMove in self.valid_moves:
                self.valid_moves.remove(rMove)

            # done w creating the territory block of 2 corners
            if state[1] == 5:
                self.done_corners = True
                self.dirty_flag = True
                
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
    # but realy, we have a lot of choices mo, so we kinda waste comp time, is also slower w all the extra math
    # O(1)
    def uct(n):
        if upper_confidence_bound:
            return (n.Q/n.N) + (2 * math.sqrt((math.log(n.parent.N) / n.N)))
        else:
            return n.Q/n.N

    if _node.children:
        best_child = (0, 0)
        for i, child in enumerate(_node.children):
            if child.fin:
                return child
            uct_val = uct(child)
            if uct_val > best_child[1]:
                best_child = (i, uct_val)
        return _node.children[best_child[0]]
    print('its just none for no children')
    return None


# O(n), it is either the timeComplexity of the best_uct_child or we need to get, create and add a new node, 
# ... wich always depens on the len and in the worst case is is the same as the input_len
def FindSpotToExpand(_node, done_opening):
    if not _node.valid_moves:
        return _node
     
    if len(_node.children) != len(_node.valid_moves):
        # toi prevent fouyl play ;) not enough time to look at all the children, so make it kinda random and so more fair
        # if len(_node.valid_moves) > 9:
        #     init_move_child = random.choice(_node.valid_moves)
        # else:
        init_move_child = _node.valid_moves[len(_node.children)]
        
        n_child = node(new_game_state(_node.state, init_move_child), 
                       _node, 
                       init_move_child, )
        n_child.valid_moves = valid_moves(n_child.state)

        if not n_child.state:
            print('I gonna error, None state child: ', n_child.init_move, _node.init_move)
        if not n_child.valid_moves:
            print('I gonna error, None Validmoves child: ', n_child.init_move, _node.init_move)

        _node.children.append(n_child)
        return n_child
    
    maxUct_child = best_uct_child(_node, True)
    return maxUct_child
        
        
# O(n), the more moves there are, the more the function grows in time    
def rollout(_node):
    
    sim_state = _node.state
    last_move = _node.init_move
    
    sim_moves = copy.copy(_node.valid_moves)
    # random.shuffle(sim_moves)
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
    


# state = np.full((19, 19), 0, dtype=int), 7
# state[0][9][9] = 2
# state[0][1][1] = 1
# state[0][5][5] = 2

# state[0][2][2] = 1
# state[0][10][5] = 2
# state[0][3][3] = 1







# start = time.perf_counter_ns()
# a = check_threats(state)
# end = time.perf_counter_ns()

# print(a)
# print('took: ', end-start)



# TODO:
# fix the cxurrent opening , remove oppesite, mnake territory
# change uct constant (test, 0-100?)
# 
# explore adjacent moves
# fix enemy moves when opening until move 11
# firt 2 are free, after, we need to check if the eney is winning?
# create a block
