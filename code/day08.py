# Import modules
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import math
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day08.txt")

# Get usable input
lr_instructions = [x for x in input[0] if x != "\n"]
nodes = {}
for line in input[2:]:
    node = line[: line.find(" ")]
    node_left = line[(line.find("(") + 1) : line.find(",")]
    node_right = line[(line.find(",") + 2) : line.find(")")]
    nodes[node] = [node_left, node_right]


# Function to get correct step from instructions list
def get_step(step, instructions=lr_instructions):
    step_modular = step % len(instructions)
    lr = instructions[step_modular]
    if lr == "L":
        return 0
    else:
        return 1


# Function to count steps from starting node to one of a list of ending nodes
def count_steps(starting_node, ending_nodes, enforce_movement=False):
    steps = 0
    current_node = starting_node
    while (current_node not in ending_nodes) or (int(enforce_movement) > steps):
        current_node = nodes[current_node][get_step(steps)]
        steps += 1
    return steps


# Get solution to part one
part_one_solution = count_steps("AAA", ["ZZZ"])

# Now list all nodes ending in A and all nodes ending in Z
starting_nodes = [x for x in nodes.keys() if x[2] == "A"]
ending_nodes = [x for x in nodes.keys() if x[2] == "Z"]

# Get list of solutions for each node ending in A
individual_solutions = [count_steps(x, ending_nodes) for x in starting_nodes]

# Get candidate part two solution
part_two_solution = math.lcm(*individual_solutions)

# Check that no individual solution ends partway through lr_instructions (validate that we can use LCM)
for x in individual_solutions:
    assert x % len(lr_instructions) == 0

# Check that each solution is on a cycle that divides the length of lr_instructions (validate that we can use LCM)
for x in ending_nodes:
    assert count_steps(x, [x], True) % len(lr_instructions) == 0

# Print solutions
print("Solution to part one:", part_one_solution)
print("Solution to part two:", part_two_solution)

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
