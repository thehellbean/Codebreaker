from itertools import product


code = '6666'  # Define the code to break here


possible_numbers = '123456789' #  All numbers that can appear in the code


code_length = 4 #  The length of the code


potentials = [''.join(p) for p in product(possible_numbers, repeat=code_length)] #  Creates a list of all possible codes


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
            continue # No match

    return [str(answer.count("B")), str(answer.count("W"))]  # Return as strings to keep everything iterable


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
        removed = len(potentials) # The total amount of potentials is the highest number of potentials possibly removed by one guess, so we use it since we want numbers as low as possible
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
    guess = "1122" # We haven't had a chance to grab information yet so we just play a combination
    for i in range(6): # The goal is to have the program solve the code in 6 or less tries, so we limit it by using a for loop instead of a while loop
        if guess == code:
            print("I got it right! It's {}".format(guess))
            break
        print("My guess is {}".format(guess))
        # The call to calcBlackWhite here can easily be replaced with a call to raw_input/input (depending on py version)
        response = calcBlackWhite(guess, code)  # To avoid human error we use the calcBlackWhite function instead of user input because users are stupid, but this can easily be replaced with a call to input()
        print("Automatically created a response of {} black and {} white".format(response[0], response[1]))
        potentials = removePotentials(guess, response, potentials)
        try:
            potentials.remove(guess)  # Remove the guess, since it obviously wasn't right
        except ValueError:  # This occurs if the guess isn't in the potentials list
            pass  # It isn't really an issue so we just pass here
        guess = calcScore(potentials)


if __name__ == '__main__':
    main(potentials)
