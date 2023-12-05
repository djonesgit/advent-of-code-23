# Import libraries
import numpy as np
import pandas as pd
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day03.txt")


# Function to check if character is a symbol
def is_symbol(symbol):
    if len(symbol) > 1:
        raise Exception("This function only checks an individual character")
    return (not symbol.isdigit()) & (symbol != ".")


# Map input to Boolean symbol assesssment
df_symbol = []
for line in input:
    line = line.replace("\n", "")
    df_symbol += [pd.Series([int(is_symbol(x)) for x in line])]
df_symbol = pd.DataFrame(df_symbol)

# Map Boolean character assessment to Boolean character adjacency
df_adjacent = pd.DataFrame(np.zeros_like(df_symbol))
(row_count, col_count) = df_symbol.shape
for row in df_adjacent.index:
    for col in df_adjacent.columns:
        if df_symbol.loc[row, col] == 1:
            row_min = max(0, row - 1)
            row_max = min(row_count - 1, row + 1)
            col_min = max(0, col - 1)
            col_max = min(col_count - 1, col + 1)
            for inner_row in range(row_min, row_max + 1):
                for inner_col in range(col_min, col_max + 1):
                    df_adjacent.loc[inner_row, inner_col] = 1

# Map input to Boolean digit assessment
df_digit = []
for line in input:
    line = line.replace("\n", "")
    df_digit += [pd.Series([int(x.isdigit()) for x in line])]
df_digit = pd.DataFrame(df_digit)

# Check which digits are adjacent to characters
df_adjacent_digit = df_digit * df_adjacent

# Ensure we've got the full number corresponding to any adjacent digits
reference = pd.DataFrame(np.zeros_like(df_symbol))
while not (reference == df_adjacent_digit).all().all():
    reference = df_adjacent_digit.copy()
    for row in df_adjacent_digit.index:
        for col in df_adjacent_digit.columns:
            if (df_digit.loc[row, col] == 1) & (df_adjacent_digit.loc[row, col] == 0):
                col_min = max(0, col - 1)
                col_max = min(col_count - 1, col + 1)
                new_value = 0
                for inner_col in range(col_min, col_max + 1):
                    new_value = max(new_value, df_adjacent_digit.loc[row, inner_col])
                df_adjacent_digit.loc[row, col] = new_value


# Function to get the numbers out of a line of input
def get_numbers(i):
    line = input[i]
    included = df_adjacent_digit.loc[i]
    output = ""
    for j in range(len(included)):
        if included[j] == 1:
            output += line[j]
        else:
            output += " "
    return output.split()


# Loop through rows and get numbers
part_numbers = []
for i in range(len(df_adjacent_digit)):
    part_numbers += get_numbers(i)
part_numbers = [int(x) for x in part_numbers]

# Print solutions
print("Solution to part one:", sum(part_numbers))
