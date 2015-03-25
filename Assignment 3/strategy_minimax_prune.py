from strategy import Strategy
from game_state import GameState
from tree import Tree


class StrategyMiniMaxPrune(Strategy):
    """
    AI Controller which determines moves based on minimax strategy
    """

    def minimax(self, state, initial_player, scores):
        """(StrategyMiniMaxPrune, GameState, str, list-of-int) -> int

        Return the maximum score if it is current player is the initial
        player, or the minimum score if current player is not.
        """

        if state.next_player == initial_player:
            return max(scores)
        return min(scores)

    def suggest_move(self, state):
        """(StrategyMiniMaxPrune, GameState) -> GameMove

        Return a move selected by minimax from the moves possible in the
        current game state
        """

        # Currently fatalistic.
        move_tree = self.generate_move_tree(state, state.next_player)
        for move in move_tree.children:
            if move.value[1] == 1:
                return move.value[0]
        for move in move_tree.children:
            if move.value[1] == 0:
                return move.value[0]
        for move in move_tree.children:
            if move.value[1] == -1:
                return move.value[0]

    def generate_move_tree(self, state, initial_player, chosen_move=None):
        """(StrategyMiniMaxPrune, GameState, str, GameMove) -> Tree

        Return a Tree ADT of the possible moves based on the current state.
        Each node's value will contain the move chosen to arrive at the node,
        and the score (1/0/-1 for a win/tie/loss) in a tuple. The children of
        the node will be the possible moves from that node.
        """
        dictionary = {}

        if state.over:
            if state.winner(initial_player):
                return Tree((chosen_move, 1))
            elif state.winner(get_opponent(initial_player)):
                return Tree((chosen_move, -1))
            else:
                return Tree((chosen_move, 0))
        else:
            possible_moves = state.possible_next_moves()
            children = []
            scores = []
            for move in possible_moves:
                new_state = state.apply_move(move)
                # Recursively generate the children of each move
                next_node = self.generate_move_tree(new_state,
                                                    initial_player, move)
                children.append(next_node)
                if self.prune(state, initial_player,next_node.value[1]):
                    return Tree((chosen_move, next_node.value[1]), children)
            for child in children:
                # Collect scores of all children
                scores.append(child.value[1])
            # Use minimax to chose assigned score
            m_score = self.minimax(state, initial_player, scores)
            return Tree((chosen_move, m_score), children)

    def prune(self, state, initial_player, score):
        """(StrategyMiniMaxPrune, GameState, str, int) -> boolean

        Return whether a branch of a move tree should be pruned
        """
        if (state.next_player is not initial_player) and score == -1:
            return True
        if (state.next_player is initial_player) and score == 1:
            return True
        return False

def get_opponent(current_player):
    """(str) -> str

    Return the opponent of the current player. Return either "p1" or "p2"

    >>> get_opponent('p1')
    'p2'
    """

    if current_player == "p1":
        return "p2"
    return "p1"

