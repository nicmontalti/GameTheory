import numpy as np
from game import Game


def alpha_eps(Ts, params, iterations=10):
    names = ['pd', 'opd', 'pdpa']

    result = []

    for name in names:
        epsTmean = []
        ATmean = []
        epsTstd = []
        ATstd = []

        for T in Ts:
            params_copy = params
            params_copy['T'] = T
            game = Game(name, params_copy)

            epss = []
            As = []

            for i in range(iterations):
                G, A = game.evolution()
                eps = (1-G)*(1-A)

                epss.append(np.mean(eps))
                As.append(np.mean(A))

            epsTmean.append(np.mean(epss))
            ATmean.append(np.mean(As))
            epsTstd.append(np.std(epss))
            ATstd.append(np.std(As))
        result.append([epsTmean, epsTstd, ATmean, ATstd, Ts])

    return result


def get_histo(G, A):
    A_1 = A * G
    A_2 = A * (1-G)

    alphas = np.linspace(0, 1, 9)
    num_alpha = np.zeros(9)
    num_alpha2 = np.zeros(9)
    for index, alpha in enumerate(alphas):
        num_alpha[index] = np.sum(A_1 == alpha)
        num_alpha2[index] = np.sum(A_2 == alpha)

        # remove zeros given by the masks
        if index == 0:
            num_alpha[0] -= np.sum(G == 0)
            num_alpha2[0] -= np.sum(G == 0)

    alpha_mean_def = np.mean(A[G.astype(bool)])
    alpha_mean_coop = np.mean(A[np.logical_not(G.astype(bool))])
    # alpha_std_def = np.std(A[G.astype(bool)])
    # alpha_std_coop = np.std(A[np.logical_not(G.astype(bool))])

    ratio_mean = alpha_mean_coop / alpha_mean_def
    # ratio_std = np.sqrt((alpha_std_coop / alpha_mean_coop) ** 2 + (alpha_std_def / alpha_mean_def)**2) * ratio_mean

    M = G.shape[0]
    N = G.shape[1]

    return num_alpha / (M*N), num_alpha2 / (M*N), ratio_mean


def correlation(params, iterations=10):
    stat_alpha1 = np.empty((iterations, 9))
    stat_alpha2 = np.empty((iterations, 9))

    game = Game('pdpa', params)

    for i in range(iterations):
        G, A = game.evolution()
        stat_alpha1[i, :], stat_alpha2[i, :], _ = get_histo(G, A)

    mean_1 = np.mean(stat_alpha1, axis=0)
    mean_2 = np.mean(stat_alpha2, axis=0)
    std_1 = np.std(stat_alpha1, axis=0)
    std_2 = np.std(stat_alpha2, axis=0)

    result = np.array([mean_1, std_1, mean_2, std_2, np.linspace(0, 1, 9)])

    return result
