# Import time
import time

# Initialise timer
tic = time.perf_counter()

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

# Map Boolean symbol assessment to Boolean symbol adjacency
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

# Get unique IDs for each number in the matrix
df_unique = pd.DataFrame(np.zeros_like(df_adjacent_digit))
count = 0
for row in df_unique.index:
    prev = 0
    for col in df_unique.columns:
        if (prev == 1) & (df_adjacent_digit.loc[row, col] == 1):
            df_unique.loc[row, col] = count
        elif df_adjacent_digit.loc[row, col] == 1:
            prev = 1
            count += 1
            df_unique.loc[row, col] = count
        elif prev == 1:
            prev = 0

# Map input to Boolean star assesssment
df_star = []
for line in input:
    line = line.replace("\n", "")
    df_star += [pd.Series([int(x == "*") for x in line])]
df_star = pd.DataFrame(df_star)

# Map Boolean star assessment to count of part adjacency
df_adjacency_count = pd.DataFrame(np.zeros_like(df_star))
(row_count, col_count) = df_star.shape
for row in df_adjacency_count.index:
    for col in df_adjacency_count.columns:
        values = []
        if df_star.loc[row, col] == 1:
            row_min = max(0, row - 1)
            row_max = min(row_count - 1, row + 1)
            col_min = max(0, col - 1)
            col_max = min(col_count - 1, col + 1)
            for inner_row in range(row_min, row_max + 1):
                for inner_col in range(col_min, col_max + 1):
                    values += [df_unique.loc[inner_row, inner_col]]
        count = len(set([int(x) for x in values if x not in [0, "0"]]))
        df_adjacency_count.loc[row, col] = count


# Loop through stars with two adjacent parts to get gear ratios
gear_ratios = []
for row in df_adjacency_count.index:
    for col in df_adjacency_count.columns:
        if df_adjacency_count.loc[row, col] == 2:
            row_min = max(0, row - 1)
            row_max = min(row_count - 1, row + 1)
            col_min = max(0, col - 1)
            col_max = min(col_count - 1, col + 1)
            gears = []
            for inner_row in range(row_min, row_max + 1):
                for inner_col in range(col_min, col_max + 1):
                    if input[inner_row][inner_col].isdigit():
                        col_offset = 1
                        keep_going = 1
                        while ((inner_col - col_offset) >= 0) & (keep_going == 1):
                            while input[inner_row][
                                inner_col - col_offset + 1
                            ].isdigit():
                                col_offset += 1
                            keep_going = 0
                        col_offset -= 1
                        gear = input[inner_row][inner_col - col_offset + 1]
                        col_progress = 1
                        while input[inner_row][
                            inner_col - col_offset + col_progress + 1
                        ].isdigit():
                            gear += input[inner_row][
                                inner_col - col_offset + col_progress + 1
                            ]
                            col_progress += 1
                        gear = int(gear)
                        gears += [gear]
            gears = list(pd.unique(pd.Series(gears)))
            if len(gears) == 1:
                gears = [gears[0], gears[0]]
            gear_ratios += [gears[0] * gears[1]]

# Print solutions
print("Solution to part one:", sum(part_numbers))
print("Solution to part two:", sum(gear_ratios))

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
