from move import Move


class TippyMove(Move):
    """ A move in the game of Tippy.

    """

    def __init__(self, x, y):
        """ (TippyMove, x, y) -> NoneType

        Initialize a new TippyMove for adding an x or o onto the grid at the
        position defined by coordinates x and y.
        """

        self.x = x
        self.y = y

    def __repr__(self):
        """ (TippyMove) -> str

        Return a string representation of TippyMove self that creates an
        equivalent TippyMove if evaluated.

        >>> m = TippyMove(1, 2)
        >>> m.__repr__()
        'TippyMove(1, 2)'
        """

        return "TippyMove({}, {})".format(self.x, self.y)

    def __str__(self):
        """ (TippyMove) -> str

        Return a convenient string representation of TippyMove self.

        >>> m = TippyMove(1, 2)
        >>> print(m)
        (1, 2)
        """

        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        """ (TippyMove, TippyMove) -> str

        Return True if and only if the TippyMove other is equivalent to the
        TippyMove self.

        >>> m = TippyMove(1, 2)
        >>> n = TippyMove(1, 2)
        >>> m == n
        True
        """

        return (isinstance(other, TippyMove) and self.x == other.x and
                self.y == other.y)

if __name__ == '__main__':
    import doctest
    doctest.testmod()