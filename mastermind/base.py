from abc import ABC, abstractmethod

class MastermindGame(ABC):
    def __init__(self, num_colors, code_length):
        self.num_colors = num_colors
        self.code_length = code_length

    @abstractmethod
    def generate_secret_code(self):
        pass


    @abstractmethod
    def guess_code(self, past_guesses, past_feedback):
        pass


    def compute_feedback(self, guess, secret):
        pegs = [''] * self.code_length
        secret_used = [False] * self.code_length
        guess_used = [False] * self.code_length

        # First pass: Black pegs (correct position and color)
        for i in range(self.code_length):
            if guess[i] == secret[i]:
                pegs[i] = 'B'
                secret_used[i] = True
                guess_used[i] = True

        # Second pass: White pegs (correct color, wrong position)
        for i in range(self.code_length):
            if not guess_used[i]:
                for j in range(self.code_length):
                    if not secret_used[j] and guess[i] == secret[j]:
                        pegs[i] = 'A'
                        secret_used[j] = True
                        break  # match each color only once        

        return pegs
    

    def run(self):
   
        secret = self.generate_secret_code()
        past_guesses = []
        past_feedbacks = []
        attempts = 0

        while True:
            guess = self.guess_code(past_guesses, past_feedbacks)
            attempts += 1
            feedback = self.compute_feedback(guess, secret)
            past_guesses.append(guess)
            past_feedbacks.append(feedback)
            if guess == secret:
                break

        return attempts
