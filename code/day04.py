# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import numpy as np
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day04.txt")

# Extract lists of numbers
card_numbers = []
winning_numbers = []
my_numbers = []
for line in input:
    card_number = int([x for x in line[: (line.find(":"))].split(" ") if x != ""][1])
    card_numbers += [card_number]
    numbers = line[(line.find(":") + 1) :]
    winning_numbers_instance = [
        int(x) for x in numbers[: numbers.find("|")].split(" ") if x != ""
    ]
    winning_numbers += [winning_numbers_instance]
    my_numbers_instance = [
        int(x)
        for x in numbers[(numbers.find("|") + 1) :].replace("\n", "").split(" ")
        if x != ""
    ]
    my_numbers += [my_numbers_instance]

# Check how many winning matches there are on each card
matches = []
for i in range(len(card_numbers)):
    matches_instance = 0
    for winning_number in winning_numbers[i]:
        for my_number in my_numbers[i]:
            if winning_number == my_number:
                matches_instance += 1
    matches += [matches_instance]

# Get scores
scores = []
for matches_instance in matches:
    if matches_instance == 0:
        scores += [0]
    else:
        scores += [2 ** (matches_instance - 1)]

# Now figure out how many of each card we should have
cards_with_multiplicity = card_numbers.copy()
for i in range(len(card_numbers)):
    card_number = card_numbers[i]
    matches_instance = matches[i]
    if matches_instance != 0:
        multiplier = len([x for x in cards_with_multiplicity if x == card_number])
        cards_to_add = []
        for j in range(1, matches_instance + 1):
            cards_to_add += [card_number + j]
        cards_with_multiplicity += list(np.repeat(cards_to_add, multiplier))


# Print solutions
print("Solution to part one:", sum(scores))
print("Solution to part two:", len(cards_with_multiplicity))

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
