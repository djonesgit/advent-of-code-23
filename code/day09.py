# Import modules
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day09.txt")

# Get input in usable format
sequences = [[int(x) for x in line.split(" ") if x != "\n"] for line in input]


# Define function to difference entries in a sequence
def difference_entry(sequence):
    output = []
    for i in range(len(sequence) - 1):
        output += [sequence[i + 1] - sequence[i]]
    return output


# Define function to get next element in a sequence
def get_next_element(sequence):
    next_entries = [sequence[len(sequence) - 1]]
    while sum([int(x != 0) for x in sequence]) > 0:
        sequence = difference_entry(sequence)
        next_entries += [sequence[len(sequence) - 1]]
    return sum(next_entries)


# Define function to reverse a sequence
def reverse_sequence(sequence):
    length = len(sequence) - 1
    return [sequence[length - i] for i in range(length + 1)]


# Get solutions
part_one_solution = sum([get_next_element(sequence) for sequence in sequences])
part_two_solution = sum(
    [get_next_element(reverse_sequence(sequence)) for sequence in sequences]
)


# Print solutions
print("Solution to part one:", part_one_solution)
print("Solution to part two:", part_two_solution)

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
