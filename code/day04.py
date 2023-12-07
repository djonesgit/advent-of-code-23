# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
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

# Print solutions
print("Solution to part one:", sum(scores))
print("Solution to part two:")

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
