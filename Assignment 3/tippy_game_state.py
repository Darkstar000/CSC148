from game_state import GameState
from tippy_move import TippyMove
from random import randint

class TippyGameState(GameState):
    """ The state of a Tippy game.
    """

    def __init__(self, p, n, grid = None, interactive = False):
        """ (TippyGameState, str, int, list of list of int, bool) -> NoneType

        Initialize TippyGameState self with player p and a grid. If no grid is
        provided, initialize an empty grid of sidelength n.
        """
        GameState.__init__(self, p)
        self.instructions = ('Players take turns placing an x or an o on the '
                             'board. The first player to complete a tippy '
                             'wins.')
        if interactive:
            n = int(input('Sidelength of the board?'))

        # Initialize the empty grid if one is not passed on.
        if not grid:
            row = []
            self.grid = []
            for i in range(n):
                row += [0]
            for i in range(n):
                self.grid.append(row[:])
        else:
            self.grid = grid

        self.over = (self.winner(self.opponent()) or
                     self.possible_next_moves() == [])

    def __repr__(self):
        """ (TippyGameState) -> str

        Return a string representation of TippyGameState self that evaluates to
        an equivalent TippyGameState.

        >>> t = TippyGameState('p1', 3)
        >>> s = t.__repr__()
        >>> s
        "TippyGameState('p1', 3, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])"
        """

        return "TippyGameState({}, {}, {})".format(repr(self.next_player),
                                                   repr(len(self.grid)),
                                                   repr(self.grid))

    def __str__(self):
        """ (TippyGameState) -> str

        Return a string representation of TippyGameState.

        >>> t = TippyGameState('p1', 5)
        >>> print(t)
        Next player: p1
          0 1 2 3 4 (y)
        0[ | | | | ]
        1[ | | | | ]
        2[ | | | | ]
        3[ | | | | ]
        4[ | | | | ]
        (x)
        """

        grid_str = " "

        # Draw the y-axis.
        for i in range(len(self.grid)):
            grid_str += ' ' + str(i)
        grid_str += ' (y)\n'

        # Draw the grid and the x-axis.
        for i in range(len(self.grid)):
            grid_str += str(i) + '['
            for element in self.grid[i]:
                if element == -1:
                    grid_str += 'x'
                elif element == 1:
                    grid_str += 'o'
                else:
                    grid_str += ' '
                grid_str += '|'
            grid_str = grid_str[:len(grid_str) - 1] + ']\n'

        grid_str += '(x)'
        return "Next player: {}\n{}".format(self.next_player, grid_str)

    def __eq__(self, other):
        """ (TippyGameState, TippyGameState) -> bool

        Return True iff TippyGameState self is equivalent to TippyGameState
        other.

        >>> q = TippyGameState('p1', 5)
        >>> r = TippyGameState('p1', 5)
        >>> s = TippyGameState('p2', 5)
        >>> t = TippyGameState('p1', 6)
        >>> q == r
        True
        >>> r == s
        False
        >>> q == t
        False
        """

        return (isinstance(other, TippyGameState) and
                self.next_player == other.next_player and
                self.grid == other.grid)

    def get_move(self):
        """ (TippyGameState) -> TippyMove

        Prompt user and return move.
        """

        coords = input("Where would you like to place your piece (in the form"+
                       " 'xy')?")
        return TippyMove(int(coords[0]), int(coords[1]))

    def apply_move(self, move):
        """ (TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyGameState by applying move to self.
        """

        if move in self.possible_next_moves():
            # Update the grid.
            new_grid = []
            for i in range(len(self.grid)):
                new_grid.append(self.grid[i][:])
            if self.next_player == 'p1':
                new_grid[move.x][move.y] = -1
            else:
                new_grid[move.x][move.y] = 1
            return TippyGameState(self.opponent(), len(self.grid), new_grid)
        else:
            return None

    def possible_next_moves(self):
        """ (TippyGameState) -> list of TippyMove

        Return a possibly empty list of moves that are legal from the present
        state.
        """

        legal_moves = []
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] == 0:
                    legal_moves.append(TippyMove(x, y))
        return legal_moves

    def winner(self, player):
        """ (TippyGameState, str) -> bool

        Return True if and only if the game is over and the player has won.

        Precondition: player is either 'p1' or 'p2'
        """
        if player == 'p1':
            return is_tippy(self.grid, -1)
        return is_tippy(self.grid, 1)

    def rough_outcome(self):
        """ (TippyGameState) -> float

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state self.
        """

        for move in self.possible_next_moves():
            # Check to see if the next player can win in a single move.
            if self.next_player == 'p1':
                self.grid[move.x][move.y] = -1
            else:
                self.grid[move.x][move.y] = 1
            if self.winner(self.next_player):
                # Undo the move.
                self.grid[move.x][move.y] = 0
                return TippyGameState.WIN

            # Check to see if the opponent can win in a single move.
            if self.next_player == 'p1':
                self.grid[move.x][move.y] = 1
            else:
                self.grid[move.x][move.y] = -1
            if self.winner(self.opponent()):
                # Undo the move.
                self.grid[move.x][move.y] = 0
                return TippyGameState.LOSE
            self.grid[move.x][move.y] = 0
        return TippyGameState.DRAW

def is_tippy(grid, player):
    """ (list of list of int) -> bool

    Return true iff a tippy is on the board placed by player.
    """

    # Go through the grid and check each square.
    for x in range(len(grid)):
        for y in range(len(grid[x])):

            # Check for tippys in every possible direction.
            for dx in range(-1, 2, 2):
                for dy in range(-1, 2, 2):

                    # Find horizontal tippys
                    if (abs(look(grid, x, y, player)
                        + look(grid, x + dx, y, player)
                        + look(grid, x + dx, y + dy, player)
                        + look(grid, x + 2 * dx, y + dy, player)) == 4):
                        return True
                    # Find vertical tippys
                    if (abs(look(grid, x, y, player)
                        + look(grid, x, y + dy, player)
                        + look(grid, x + dx, y + dy, player)
                        + look(grid, x + dx, y + 2 * dy, player)) == 4):
                        return True
    return False

def look(grid, x, y, player):
    """ (list of list of int, int, int, int, int, int) -> int

    Helper function for the function is_tippy. Return an int value for
    """

    # x and y are out of bounds
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid):
        return 0
    if grid[x][y] != player:
        return 0
    return 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()
