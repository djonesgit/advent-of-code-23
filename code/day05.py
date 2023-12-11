# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day05.txt")

# Get input seed numbers
input_seeds = [
    int(x) for x in input[0].replace("\n", "").split(" ") if "seeds" not in x
]

# Extract maps
maps = {}
name = ""
names = []
for line in input:
    line = line.replace("\n", "")
    if ":" in line:
        if name != "":
            maps[name] = map_instance
        if "seeds" not in line:
            name = line[: line.find("map")].replace(" ", "")
            names += [name]
        map_instance = []
    if (line != "") & (":" not in line):
        map_instance += [[int(x) for x in line.split(" ")]]
maps[name] = map_instance


# Helper function to map using the stored maps
def map_using_maps(input_values, map_name):
    map_instance = maps[map_name]
    output = []
    for input_value in input_values:
        output_instance = []
        for triple in map_instance:
            if (input_value >= triple[1]) & (input_value < (triple[1] + triple[2])):
                output_instance += [triple[0] + input_value - triple[1]]
        if len(output_instance) == 0:
            output_instance += [input_value]
        output += output_instance
    return output


# Function to map all the way through
def map_all_way(input_values):
    for name in names:
        input_values = map_using_maps(input_values, name)
    return input_values


# Get part one solution
map_outputs = map_all_way(input_seeds)
part_one_solution = min(map_outputs)


# Helper function to map overlapping portion of range
def map_overlap(range_double, range_triple):
    unmapped = []
    mapped = []
    # Get portion below range_triple
    if range_double[0] < range_triple[1]:
        lower = range_double[0]
        if range_double[1] >= range_triple[1]:
            upper = range_triple[1] - 1
        else:
            upper = range_double[0] + range_double[1] - 1
        unmapped += [[lower, upper - lower + 1]]
    # Get portion above range_triple
    if range_double[0] + range_double[1] - 1 >= range_triple[1] + range_triple[2]:
        upper = range_double[0] + range_double[1] - 1
        if range_double[0] < range_triple[1] + range_triple[2]:
            lower = range_triple[1] + range_triple[2]
        else:
            lower = range_double[0]
        unmapped += [[lower, upper - lower + 1]]
    # Get overlapping portion
    if range_double[0] + range_double[1] - 1 >= range_triple[1]:
        if range_double[0] < range_triple[1] + range_triple[2]:
            lower = max(range_double[0], range_triple[1])
            upper = min(
                range_double[0] + range_double[1] - 1,
                range_triple[1] + range_triple[2] - 1,
            )
            lower_mapped = lower - range_triple[1] + range_triple[0]
            upper_mapped = upper - range_triple[1] + range_triple[0]
            mapped += [lower_mapped, upper_mapped - lower_mapped + 1]
    return unmapped, mapped


# Helper function to map ranges to ranges
def map_ranges_to_ranges(range_doubles, map_name):
    map_instance = maps[map_name]
    output_mapped = []
    doubles_to_check = range_doubles
    for triple in map_instance:
        doubles_to_track = []
        for range_double in doubles_to_check:
            new_doubles, output_instance = map_overlap(range_double, triple)
            doubles_to_track += new_doubles
            output_mapped += [output_instance]
        doubles_to_check = doubles_to_track
    output_unmapped = new_doubles
    output = [x for x in output_unmapped + output_mapped if x != []]
    return output


# Function to map ranges all the way through
def map_range_all_way(input_values):
    input_doubles = []
    for i in range(int(len(input_values) / 2)):
        input_doubles += [[input_values[2 * i], input_values[(2 * i) + 1]]]
    for name in names:
        input_doubles = map_ranges_to_ranges(input_doubles, name)
    return input_doubles


# Get part two solution
range_outputs = map_range_all_way(input_seeds)
part_two_solution = min([x[0] for x in range_outputs])


# Print solutions
print("Solution to part one:", part_one_solution)
print("Solution to part two:", part_two_solution)

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
