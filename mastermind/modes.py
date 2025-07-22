import numpy as np
import random

# Mixin for beginner mode guessing strategy
class BeginnerModeMixin:
    def guess_code(self, past_guesses, past_feedback):
        fixed_positions = {}   # Tracks positions with black pegs (correct color and position)
        white_candidates = {}   # Tracks colors known to be in the code, but not in specific positions
        eliminated_colors = set() # Tracks colors that are not in the code
        used_colors = set() # Tracks all colors confirmed to be in the code

        # Analyze past guesses and feedback
        for guess, feedback in zip(past_guesses, past_feedback):
            for index, (color, peg) in enumerate(zip(guess, feedback)):
                if peg == 'B':
                    # Black peg: correct color in correct position
                    fixed_positions[index] = color
                    used_colors.add(color)
                    # If this color was previously a white candidate, remove it
                    if color in white_candidates:
                        del white_candidates[color]  # remove from white if now black
                elif peg == 'A':
                    # White peg: correct color, wrong position
                    if color not in fixed_positions.values():
                        if color not in white_candidates:
                            white_candidates[color] = set()
                        white_candidates[color].add(index) # Exclude current index
                        used_colors.add(color)
                elif peg == '':
                    # No peg: color is not in the code
                    eliminated_colors.add(color)

        # Build current guess
        guess = [None] * self.code_length
        available_positions = set(range(self.code_length)) # Positions not yet filled

        # Place colors with known fixed positions (black pegs)
        for index, color in fixed_positions.items():
            guess[index] = color
            available_positions.discard(index)

        # Sort white peg candidates by how many positions they can still occupy
        sorted_candidates = sorted(
            white_candidates.items(),
            key=lambda item: len(available_positions - item[1])
        )

        # Attempt to place white peg colors into valid positions
        for color, banned_indices in sorted_candidates:
            possible_positions = list(available_positions - banned_indices)
            if possible_positions:
                pos = np.random.choice(possible_positions)
                guess[pos] = color
                available_positions.discard(pos)

        # Fill any remaining positions with random, non-eliminated colors
        all_colors = set(range(self.num_colors))
        valid_colors = list(all_colors - eliminated_colors)

        for index in available_positions:
            guess[index] = np.random.choice(valid_colors)

        return guess


# Mixin for standard mode guessing strategy (uses feedback consistency)
class StandardModeMixin:
    def guess_code(self, past_guesses, past_feedback):
        digits = np.arange(0, self.num_colors) # All possible colors
        grids = np.meshgrid(*[digits] * self.code_length, indexing='ij')  # Create a full grid of guesses
        codes = None # Will hold all candidate codes

        # Helper function to count black and white pegs
        def get_pegs(feedback):
            return feedback.count('B'), feedback.count('A')
        
        # Generate all possible codes depending on repetition policy
        if not self.allow_repeats:
            # Generate permutations (no repeats)
            def build_perms(curr, remaining):
                if len(curr) == self.code_length:
                    return [curr]
                perms = []
                for i, val in enumerate(remaining):
                    perms.extend(build_perms(curr + [val], np.delete(remaining, i)))
                return perms
            perms = build_perms([], digits)
            codes = np.array(perms)
        else:
            # Generate combinations with repeats allowed
            codes = np.stack(grids, axis=-1).reshape(-1, self.code_length)

        # Convert codes to list format and exclude already guessed codes
        codes = codes.tolist()
        codes = [code for code in codes if code not in past_guesses]
        
        # If no feedback yet, make a random initial guess
        if not past_feedback:
            return random.sample(list(range(self.num_colors)), self.code_length)
        
        # Get peg counts from the last feedback
        last_feedback = get_pegs(past_feedback[-1])

        # Filter codes that would produce the same feedback if they were the secret
        all_possible_codes = [
            code for code in codes
            if get_pegs(self.compute_feedback(past_guesses[-1], code)) == last_feedback
        ]
        # Return the first consistent code

        return list(all_possible_codes[0])


