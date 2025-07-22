from .repetition import RepetitionGame, NoRepetitionGame
from .modes import BeginnerModeMixin, StandardModeMixin


class BeginnerRepetitionGame(BeginnerModeMixin, RepetitionGame):
    def __init__(self, num_colors, code_length):
        super().__init__(num_colors, code_length)
        self.allow_repeats = True


class BeginnerNoRepetitionGame(BeginnerModeMixin, NoRepetitionGame):
    def __init__(self, num_colors, code_length):
        super().__init__(num_colors, code_length)
        self.allow_repeats = False



class StandardRepetitionGame(StandardModeMixin, RepetitionGame):
    def __init__(self, num_colors, code_length):
        super().__init__(num_colors, code_length)
        self.allow_repeats = True



class StandardNoRepetitionGame(StandardModeMixin, NoRepetitionGame):
    def __init__(self, num_colors, code_length):
        super().__init__(num_colors, code_length)
        self.allow_repeats = False


def create_game(num_colors, code_length, allow_repeats, mode):
    if mode == "beginner" and allow_repeats:
        return BeginnerRepetitionGame(num_colors, code_length)
    elif mode == "beginner" and not allow_repeats:
        return BeginnerNoRepetitionGame(num_colors, code_length)
    elif mode == "standard" and allow_repeats:
        return StandardRepetitionGame(num_colors, code_length)
    elif mode == "standard" and not allow_repeats:
        return StandardNoRepetitionGame(num_colors, code_length)
    else:
        raise ValueError("Invalid mode or repetition flag")
