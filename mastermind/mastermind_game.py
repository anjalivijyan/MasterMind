import numpy as np
from .factory import create_game

def run_simulations(num_colors, code_length, allow_repeats, mode, num_simulations):
    attempts_list = []

    for _ in range(num_simulations):
        attempts = simulate_one_game(num_colors, code_length, allow_repeats, mode)
        attempts_list.append(attempts)

    return {
        'avg': np.mean(attempts_list),
        'std': np.std(attempts_list),
        'max': np.max(attempts_list),
    }


def simulate_one_game(num_colors, code_length, allow_repeats, mode):
    game = create_game(num_colors, code_length, allow_repeats, mode)
    return game.run()





