# Go-Moku Project Imports
import time
from mcts_utils import node, BackupValue, best_uct_child, FindSpotToExpand , rollout
from gmAIgent import opening_star_points, best_sequence_moves, get_valid_moves


class gmPlayer_AI:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_

    # O(1), this doesn't explanation
    def new_game(self, black_: bool):
        """ At the start of each new game you will be notified by the competition.
            this method has a boolean parameter that informs your agent whether you
            will play black or white.
        """
        self.black = black_
        self.valid_moves = opening_star_points(5, bsize=19)
        self.cluster_moves = dict()
        self.opening_done = False
        self.pref_attack = True
        
    # O(n), We do a lot in this function, but the highest TimeComplexity is O(n)
    def move(self, state, last_move, max_time_to_move = 1000):
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        start_time = time.time()

        me = 2 if self.black else 1
        enemy = 1 if self.black else 2
        
        if state[1] == 1:
            return get_valid_moves(state)[0]
        
        if self.valid_moves:
            if last_move in self.valid_moves:
                self.valid_moves.remove(last_move)
        
        # there is a chance the last item got removed out of the list a couple lines ago
        if not self.valid_moves: 
            if not self.opening_done:
                self.opening_done = True
                
            if self.opening_done:
                self.valid_moves = get_valid_moves(state, True, 2, me)
        else:
            # if the self.prev_attack is True. The AI will always play a winning 
            # node or prefer an attacking move over a defending move. 
            # And if the self.prev_attack is False its the other way around.
            
            # By changing the values of the last parameter of the 'be...moves' function
            # .. you can kinda change how fierce the AI attacks or defends
            self.cluster_moves['defence'] = best_sequence_moves(state, enemy, 3)
            self.cluster_moves['attack'] = best_sequence_moves(state, me, 2)

            if self.opening_done:
                if self.pref_attack:
                    if self.cluster_moves['attack']:
                        self.valid_moves = self.cluster_moves['attack']
                    elif self.cluster_moves['defence']:
                        self.valid_moves = self.cluster_moves['defence']
                    else:
                        self.valid_moves = get_valid_moves(state, True, 2, me)
                else:
                    if self.cluster_moves['defence']:
                        self.valid_moves = self.cluster_moves['defence']
                    elif self.cluster_moves['attack']:
                        self.valid_moves = self.cluster_moves['attack']
                    else:
                        self.valid_moves = get_valid_moves(state, True, 2, me)
                        
        n_root = node(state, None, last_move)
        n_root.valid_moves = self.valid_moves        
        
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
    