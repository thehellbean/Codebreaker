from itertools import product

# All numbers that can appear in the code
possible_numbers = (1, 2, 3, 4, 5, 6)

# The length of the code
code_length = 4

# Create a list of all possible codes
potentials = [p for p in product(possible_numbers, repeat=code_length)]


def calcBlackWhite(guess, answer):
    # This function calculates what the black/white peg combination is for a given guess/answer combination
    guess = list(guess)
    answer = list(answer)
    for g in range(4):
        if guess[g] == answer[g]:
            guess[g] = answer[g] = "B"  # Mark as used
    for g in range(4):
        try:
            i = answer.index(guess[g])
            if answer[i] == "B":  # Already used
                continue
            guess[g] = answer[i] = "W"  # Mark as used
        except ValueError:
            continue  # No match
    return [(answer.count("B")), (answer.count("W"))]


def removePotentials(guess, blackwhite, potentials):
    # This function removes all potential solutions that don't match with the data we have
    potentials = [pot for pot in potentials if calcBlackWhite(guess, pot) == blackwhite]
    return potentials
    

def calcRemovedPotentials(guess, blackwhite, potentials):
    # This function calculates how many potential solutions are removed without actually removing them
    result = 0
    for pot in potentials:
        if calcBlackWhite(guess, pot) != blackwhite:
            result += 1
    return result


def calcScore(potentials):
    # This function calculates the score of a guess and minmaxes to get the best result
    # Since the goal is to remove potentials, the best guess is the one that removes the most potentials
    if len(potentials) == 1:
        return potentials[0]
    highest = 0
    for poss in potentials:
        # The total amount of potentials is the highest number of potentials possibly removed by one guess
        # so we use it since we want numbers as low as possible
        removed = len(potentials)
        for white in range(5):
            for black in range(5 - white):
                # We test the amount of potentials removed for possible amount of black/white pegs for each potential
                # For example, we test how many potentials are removed if we guess 1111 and we get the answer [0, 0]
                calc = calcRemovedPotentials(poss, [str(black), str(white)], potentials)
                # The reason the lowest value is selected is because we're trying to get the worst case scenario
                if calc < removed:
                    removed = calc
        # We select the worst case scenario with the best result, thus minmaxing fully
        if removed > highest:
            best_guess = poss
            highest = removed
    return best_guess


def main(potentials):
    # We haven't had a chance to grab information yet so we just play a combination
    guess = (1, 1, 2, 2)
    # 6 since the goal is to have the code be solved within 6 guesses
    for i in range(6):  
        readable_guess = ','.join(str(g) for g in guess).replace(",", "")
        print("My guess is {}".format(readable_guess))
        print("How many did I get right?")
        print("Answer like so: B W where B is the amount of black pegs and W is white pegs")
        # Take user input, split it up so we get the B and W values, and turn them into integers
        response = map(lambda x: int(x), raw_input().split(' '))
        if response[0] == 4:
            print("I got it right!")
            break
        potentials = removePotentials(guess, response, potentials)
        try:
            potentials.remove(guess)
        # This occurs if the guess has already been removed
        except ValueError:
            # It isn't really an issue so we just pass here
            pass
        guess = calcScore(potentials)


if __name__ == '__main__':
    main(potentials)
