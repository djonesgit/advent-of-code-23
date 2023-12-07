# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day02.txt")


# Return all digits in a string conctenated into a single number
def find_number(string):
    number = [x for x in string if x.isdigit()]
    output = ""
    for x in number:
        output += x
    return int(output)


# Function to find game number
def find_game_number(game):
    game_number = game[: game.find(":")]
    return find_number(game_number)


# Function to split each line into subgames
def split_games(game):
    subgames = game[(game.find(":") + 1) :].strip()
    subgames = subgames.split(";")
    subgames = [x.strip() for x in subgames]
    return subgames


# Function to split subgames into colours
def split_subgames(subgame):
    red, green, blue = 0, 0, 0
    colours = [x.strip() for x in subgame.split(",")]
    for colour in colours:
        if "red" in colour:
            red = find_number(colour)
        if "green" in colour:
            green = find_number(colour)
        if "blue" in colour:
            blue = find_number(colour)
    return red, green, blue


# Function to check the maximum number for each colour in a game
def check_max_numbers(game):
    subgames = split_games(game)
    rmax, gmax, bmax = 0, 0, 0
    for subgame in subgames:
        red, green, blue = split_subgames(subgame)
        rmax, gmax, bmax = max(rmax, red), max(gmax, green), max(bmax, blue)
    return rmax, gmax, bmax


# Function to get the power of each game
def get_power(game):
    red, green, blue = check_max_numbers(game)
    return red * green * blue


# Define limits
limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


# Function to check whether a game is valid
def check_game_valid(game, limits=limits):
    red, green, blue = check_max_numbers(game)
    return (
        (red <= limits["red"]) & (green <= limits["green"]) & (blue <= limits["blue"])
    )


# Loop through games to see which games are possible
valid_games = []
game_powers = []
for game in input:
    game_powers += [get_power(game)]
    if check_game_valid(game):
        valid_games += [find_game_number(game)]

# Add together game numbers
print("Solution to part one:", sum(valid_games))
print("Solution to part two:", sum(game_powers))

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
