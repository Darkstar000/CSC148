# Taken from CSC148 Lab #5


class Tree:
    ''' Represent a Bare-bones Tree ADT'''

    def __init__(self, value=None, children=None):
        """ (Tree, object, list-of-Tree) -> NoneType

        Create Tree(self) with root containing value and
        0 or more children Trees.
        """
        self.value = value
        # copy children if not None
        self.children = children.copy() if children else []
        # the functional if  on the line above is equivalent to:
       #if not children:
           #self.children = []
       #else:
           #self.children = children.copy()

    def __repr__(self):
        """ (Tree) -> str

        Return representation of Tree (self) as string that
        can be evaluated into an equivalent Tree.

        >>> t1 = Tree(5)
        >>> t1
        Tree(5)
        >>> t2 = Tree(7, [t1])
        >>> t2
        Tree(7, [Tree(5)])
        """
        # Our __repr__ is recursive, because it can also be called via repr...!
        return ('Tree({}, {})'.format(repr(self.value), repr(self.children))
                if self.children
                else 'Tree({})'.format(repr(self.value)))

    def __eq__(self, other):
        """ (Tree, object) -> bool

        Return whether this Tree is equivalent to other.


        >>> t1 = Tree(5)
        >>> t2 = Tree(5, [])
        >>> t1 == t2
        True
        >>> t3 = Tree(5, [t1])
        >>> t2 == t3
        False
        """
        return (isinstance(other, Tree) and
                self.value == other.value and
                self.children == other.children)
