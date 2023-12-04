# Import libraries
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day01.txt")


# Function to return the output for a single string
def return_single_output(string):
    output = [x for x in string if x.isdigit()]
    output = output[0] + output[-1]
    return int(output)


# Function to run through all lines
def return_summed_output(lines):
    output = 0
    for line in lines:
        output += return_single_output(line)
    return output


# Define mapping dictionary from words to numerals
# (Note that e.g. "eighthree" should return both 8 and 3, hence the specific mapping below)
number_dict = {
    "one": "on1ne",
    "two": "tw2wo",
    "three": "thre3hree",
    "four": "fou4our",
    "five": "fiv5ive",
    "six": "si6ix",
    "seven": "seve7even",
    "eight": "eigh8ight",
    "nine": "nin9ine",
}

# Get modified input file
input_modified = []
for line in input:
    for key, value in number_dict.items():
        line = line.replace(key, value)
    input_modified += [line]

# Calculate solutions
solution_one = return_summed_output(input)
solution_two = return_summed_output(input_modified)

# Print solutions
print("Solution to part one:", solution_one)
print("Solution to part two:", solution_two)
