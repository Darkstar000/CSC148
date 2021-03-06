class GameView:
    '''
    A game view for a two-player, sequential move, zero-sum,
    perfect-information game.
    '''

    def __init__(self, state, strategy):
        '''(GameView, GameState.__class__,
            Strategy.__class__) -> NoneType

        Create GameView self for game described by state, where
        computer uses given strategy.
        '''
        player = input('Type c if you wish the computer to play first ')
        if player == 'c':
            p = 'p2'
        else:
            p = 'p1'
        if state == SubtractSquareState:
            self.state = state(p, interactive=True)
        elif state == TippyGameState:
            self.state = state(p, 3, None, interactive=True)
        self.strategy = strategy(interactive=True)

    def play(self):
        ''' (GameView) -> NoneType

        Play a game.
        '''
        print(self.state.instructions)
        print(self.state)
        print()
        while not self.state.over:
            if self.state.next_player == 'p1':
                m = self.state.get_move()
                while not m in self.state.possible_next_moves():
                    # The move was illegal.
                    print('Illegal move: {}\nPlease try again.\n'.format(m))
                    print(self.state.instructions)
                    print(self.state)
                    m = self.state.get_move()
                print('You choose: {}'.format(m))
            else:
                # The computer makes a move.
                import timeit
                start = timeit.default_timer()
                m = self.strategy.suggest_move(self.state)
                stop = timeit.default_timer()
                print("The runtime is: {}".format(stop-start))
                print('The computer chooses: {}'.format(m))
            self.state = self.state.apply_move(m)
            print('New game state: ', str(self.state))
            print()

        if self.state.winner('p2'):
            # p2, the computer, wins
            print('Beat ya!')
        elif self.state.winner('p1'):
            # p1, the human challenger, wins
            print('Congrats -- you won!!')
        else:
            print('We tied...')


if __name__ == '__main__':
    from subtract_square_state import SubtractSquareState
    from tippy_game_state import TippyGameState
    game_state = ({'s': SubtractSquareState, 't': TippyGameState})
    from strategy_random import StrategyRandom
    from strategy_minimax import StrategyMiniMax
    from strategy_minimax_prune import StrategyMiniMaxPrune
    from strategy_minimax_memoize import StrategyMiniMaxMemoize
    strategy = ({'r': StrategyRandom, 'm': StrategyMiniMax, 'mm':
        StrategyMiniMaxMemoize, 'mp': StrategyMiniMaxPrune})
    g = ''
    while not g in game_state.keys():
        g = input('s to play Subtract Square, t to play Tippy: ')
    s = ''
    while not s in strategy.keys():
        s = input('r for random strategy for computer, m for minimax, mm for '
                  'minimax_memoize:, mp for minimax_prune')
    GameView(game_state[g], strategy[s]).play()