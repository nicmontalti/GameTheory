import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random


class Game():
    def __init__(self, game, params, size=(50, 50)):
        self.name = game
        self.T = params['T']
        self.R = params['R']
        self.S = params['S']
        self.P = params['P']
        self.L = params['L']
        self.noise = params['noise']

        assert (size[0] % 2 == 0)
        assert (size[1] % 2 == 0)
        self.M = size[0]
        self.N = size[1]

        self.A0 = self._A_init(game)
        self.G0 = self._G_init()

    def _A_init(self, game):
        if game == 'pd' or game == 'sd':
            A0 = np.zeros((self.M, self.N))
        elif game == 'pdpa' or game == 'sdpa':
            A0 = np.random.randint(0, 8, (self.M, self.N)) / 8
        elif game == 'opd' or game == 'osd':
            A0 = (np.random.rand(self.M, self.N) < 0.5).astype('int')
        else:
            A0 = np.zeros()
        return A0

    def _G_init(self):
        G0 = np.random.randint(0, 2, (self.M, self.N))
        return G0

    def _neumann(self, i, j):
        left = (i - 1) % self.M
        right = (i + 1) % self.M
        up = (j + 1) % self.N
        down = (j - 1) % self.N
        result = [(left, j), (right, j), (i, up), (i, down)]
        random.shuffle(result)
        return result

    def _play(self, g1, g2, a1, a2):
        # if one of the two players doesn't play => both don't play
        if np.random.rand() < a1 or np.random.rand() < a2:
            return self.L, self.L
        else:
            if g1 == 0 and g2 == 0:
                return self.R, self.R
            elif (g1 == 0 and g2 == 1):
                return self.S, self.T
            elif (g1 == 1 and g2 == 0):
                return self.T, self.S
            elif (g1 == 1 and g2 == 1):
                return self.P, self.P

    def _play_a_turn(self, G, A):
        # evaluation of payoffs
        payoff = np.zeros((self.M, self.N))
        for j in range(self.M):
            for i_ in range(int(self.N/2)):
                i = j % 2 + i_ * 2
                neighbours = self._neumann(i, j)
                for neighbour in neighbours:
                    pay1, pay2 = self._play(
                        G[i, j], G[neighbour[0], neighbour[1]], A[i, j], A[neighbour[0], neighbour[1]])
                    payoff[i, j] += pay1
                    payoff[neighbour[0], neighbour[1]] += pay2
        return payoff

    def _imitate(self, payoff, G, A):
        G1 = G.copy()
        A1 = A.copy()
        for i in range(self.N):
            for j in range(self.M):
                if np.random.rand() < self.noise:
                    G1[i, j] = 1 - G[i, j]
                    # G1[i, j] = int(np.random.rand() < q)
                else:
                    max = payoff[i, j]
                    maxcoor = (i, j)
                    for neighbour in self._neumann(i, j):
                        if payoff[neighbour[0], neighbour[1]] > max:
                            max = payoff[neighbour[0], neighbour[1]]
                            maxcoor = (neighbour[0], neighbour[1])
                    # if maxcoor != (i,j):
                    G1[i, j] = G[maxcoor[0], maxcoor[1]]
                    A1[i, j] = A[maxcoor[0], maxcoor[1]]

        return G1, A1

    def evolution(self, timesteps=200, plot=False):
        G = self.G0.copy()
        A = self.A0.copy()

        if plot:
            fig = plt.figure(figsize=(20, 7))
            axs = fig.subplots(1, 3)

            cmap_G = matplotlib.colors.ListedColormap(['tab:green', 'tab:red'])
            cmap_A = matplotlib.colors.LinearSegmentedColormap.from_list("", [
                                                                         'ivory', 'gold'])

            im_G = axs[0].imshow(G, cmap=cmap_G)
            im_A = axs[1].imshow(A, cmap=cmap_A)
            im_eps = axs[2].imshow((1-G)*(1-A), cmap='Blues')

            cbar = fig.colorbar(im_G, ax=axs[0], ticks=[
                                0.25, 0.75], fraction=0.03, pad=0.05)
            cbar.ax.set_yticklabels(['Coop', 'Defect'])
            fig.colorbar(im_A, ax=axs[1], fraction=0.03, pad=0.05)
            fig.colorbar(im_eps, ax=axs[2], fraction=0.03, pad=0.05)

            axs[0].set_title('Strategy')
            axs[1].set_title('Abstention')
            axs[2].set_title('Cooperation')

            plt.show(block=False)

        for t in range(timesteps):
            if plot:
                fig.suptitle('R = {}, S = {}, T = {}, P = {}, L = {} \n Game: {}, noise = {} \n time={}'.format(
                    self.R, self.S, self.T, self.P, self.L, self.name, self.noise, t))
            payoff = self._play_a_turn(G, A)
            G, A = self._imitate(payoff, G, A)
            eps = (1-G)*(1-A)
            if plot:
                im_G.set_data(G)
                im_A.set_data(A)
                im_eps.set_data(eps)
                if t == timesteps-1:
                    plt.show(block=True)
                plt.pause(0.000000000001)

        return G, A

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
