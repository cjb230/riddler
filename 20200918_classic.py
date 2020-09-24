""" Solves https://fivethirtyeight.com/features/can-you-break-a-very-expensive-centrifuge/ :

One of Ollie’s favorite online games is Guess My Word. Each day, there is a secret word, and you try to guess it as
efficiently as possible by typing in other words. After each guess, you are told whether the secret word is
alphabetically before or after your guess. The game stops and congratulates you when you have guessed the secret word.
For example, the secret word was recently “nuance,” which Ollie arrived at with the following series of nine guesses:
naan, vacuum, rabbi, papa, oasis, nuclear, nix, noxious, nuance.

Each secret word is randomly chosen from a dictionary with exactly 267,751 entries. If you have this dictionary
memorized, and play the game as efficiently as possible, how many guesses should you expect to make to guess the secret
word?"""

INITIAL_LOWER_BOUND = 1
INITIAL_UPPER_BOUND = 267751


def guess_feedback(target, guess):
    if guess < target:
        return 'LOW'
    elif guess > target:
        return 'HIGH'
    elif target == guess:
        return 'CORRECT'


def guess_sequence(target):
    current_upper_bound = INITIAL_UPPER_BOUND
    current_lower_bound = INITIAL_LOWER_BOUND
    all_guesses = []
    guess_iter = 0
    still_guessing = True
    while still_guessing:
        guess_iter += 1
        guess = int(round(current_lower_bound + ((current_upper_bound - current_lower_bound) / 2)))
        all_guesses.append(guess)
        feedback = guess_feedback(target, guess)
        if feedback == 'LOW':
            current_lower_bound = guess + 1
        elif feedback == 'HIGH':
            current_upper_bound = guess - 1
        elif feedback == 'CORRECT':
            still_guessing = False
    return [guess_iter, all_guesses]


def main():
    all_possibilities = dict()
    tally = dict.fromkeys(range(1, 21),0 )
    for this_target in range(INITIAL_LOWER_BOUND, INITIAL_UPPER_BOUND+1):
        this_result = guess_sequence(this_target)
        all_possibilities[this_target] = this_result
        tally[this_result[0]] = tally[this_result[0]] + 1
    print('Number of guesses: times occurred')
    print(tally)
    print()
    total_steps = sum([key * value for key, value in tally.items()])
    print('Mean guesses = ' + str(round((total_steps / INITIAL_UPPER_BOUND),2)))
    most_common_val = max(tally, key=lambda key: tally[key])
    print('Mode guesses = ' + str(most_common_val))


if __name__ == "__main__":
    main()
