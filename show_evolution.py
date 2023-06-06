from Game import Game

if __name__ == '__main__':
    params = {
        'T': 1.5,
        'R': 1,
        'S': 0,
        'P': 0.3,
        'L': 0.4,
        'noise': 0.001
    }

    game = Game('pdpa', params)
    game.evolution(plot=True)
