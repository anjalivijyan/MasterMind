import random
from .base import MastermindGame

class RepetitionGame(MastermindGame):
    def generate_secret_code(self):
        colors = list(range(self.num_colors))
        return [random.choice(colors) for _ in range(self.code_length)]

class NoRepetitionGame(MastermindGame):
    def generate_secret_code(self):
        colors = list(range(self.num_colors))
        return random.sample(colors, self.code_length)
