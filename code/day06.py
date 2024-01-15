# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day06.txt")


# Define function to get times and distances for each race
def get_numbers(line):
    return [int(x) for x in line.split(" ") if (":" not in x) and (x != "")]


# Get times and distances for each race
times = get_numbers(input[0])
distances = get_numbers(input[1])


# Get possible distances for each time
def get_possible_distances(time):
    output = []
    for i in range(time + 1):
        output += [i * (time - i)]
    return output


# Count number of ways to win
def number_of_ways_to_win(time, distance):
    possible_distances = get_possible_distances(time)
    return sum([x > distance for x in possible_distances])


# Count number of ways to win across all races
def number_of_ways_to_win_all_races(times_list, distances_list):
    output = []
    for x, y in zip(times_list, distances_list):
        output += [number_of_ways_to_win(x, y)]
    return output


# Get product of a list
def get_product(input_list):
    output = 1
    for x in input_list:
        output *= x
    return output


# Get concatenation of times and distances
def concat_list(input_list):
    output = ""
    for x in input_list:
        output += str(x)
    output = output.replace(" ", "")
    output = [int(output)]
    return output


# Get solutions
solution_one = get_product(number_of_ways_to_win_all_races(times, distances))
solution_two = get_product(
    number_of_ways_to_win_all_races(concat_list(times), concat_list(distances))
)

# Print solutions
print("Solution to part one:", solution_one)
print("Solution to part two:", solution_two)

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
