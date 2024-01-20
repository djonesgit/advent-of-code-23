# Import time
import time

# Initialise timer
tic = time.perf_counter()

# Import libraries
import pandas as pd
import utilities as ut

# Get input file
input = ut.get_line_strings("inputs/day07.txt")

# Get lists of hands and bids
hands = []
bids = []
for line in input:
    hands += [line[: line.find(" ")]]
    bids += [int(line[(line.find(" ") + 1) :])]

# Ensure that the hands are all unique
assert len(hands) == len(set(hands))

# Define dictionary of hand-bid correspondence
hand_bid = {}
for hand, bid in zip(hands, bids):
    hand_bid[hand] = bid


# Define function to count instances of a character in a string
def count_characters(string, character):
    output = 0
    for x in string:
        if x == character:
            output += 1
    return output


# Define function to summarise hand
def summarise_hand(hand):
    cards = []
    for card in hand:
        cards += [card]
    cards = set(cards)
    output = {}
    for card in cards:
        output[card] = count_characters(hand, card)
    return output


# Define function to get hand value
def get_hand_value(hand):
    summary = summarise_hand(hand)
    if 5 in summary.values():
        return 7  # 5 of a kind
    elif 4 in summary.values():
        return 6  # 4 of a kind
    elif 3 in summary.values():
        if 2 in summary.values():
            return 5  # full house
        else:
            return 4  # 3 of a kind
    elif 2 in summary.values():
        if len(summary.values()) == 3:
            return 3  # two pair
        else:
            return 2  # pair
    else:
        return 1  # high card


# Card value dictionary
card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


# Define function to get the value of a specific card
def get_card_value(hand, location, card_vals):
    return card_vals[hand[location]]


# Create dataframe of all relevant information
df = pd.DataFrame({"hand": hands, "bid": bids})
df["hand_value"] = df["hand"].apply(get_hand_value)
for i in range(len(hands[0])):
    colname = "card" + str(i + 1) + "_value"
    df[colname] = df["hand"].apply(lambda x: get_card_value(x, i, card_values))

# Sort dataframe
df = df.sort_values(
    [
        "hand_value",
        "card1_value",
        "card2_value",
        "card3_value",
        "card4_value",
        "card5_value",
    ],
    ascending=True,
)

# Reset index and get rank and winnings
df = df.reset_index(drop=True)
df["rank"] = [x + 1 for x in df.index]
df["winnings"] = df["bid"] * df["rank"]

# Define updated card values
card_values_new = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


# Define function to find strongest hand value based on joker
def get_strongest_hand_value(hand):
    strongest_value = get_hand_value(hand)
    hand_permutations = [hand]
    for i in range(len(hand)):
        if hand[i] == "J":
            temporary_hand_permutations = hand_permutations.copy()
            for hand_permutation in temporary_hand_permutations:
                for card in card_values_new.keys():
                    new_hand_permutation = (
                        hand_permutation[:i] + card + hand_permutation[(i + 1) :]
                    )
                    hand_permutations += [new_hand_permutation]
    for hand_permutation in set(hand_permutations):
        strongest_value = max(strongest_value, get_hand_value(hand_permutation))
    return strongest_value


# Create new dataframe
df_new = pd.DataFrame({"hand": hands, "bid": bids})
df_new["hand_value"] = df_new["hand"].apply(get_strongest_hand_value)
for i in range(len(hands[0])):
    colname = "card" + str(i + 1) + "_value"
    df_new[colname] = df_new["hand"].apply(
        lambda x: get_card_value(x, i, card_values_new)
    )

# Sort dataframe
df_new = df_new.sort_values(
    [
        "hand_value",
        "card1_value",
        "card2_value",
        "card3_value",
        "card4_value",
        "card5_value",
    ],
    ascending=True,
)

# Reset index and get rank and winnings
df_new = df_new.reset_index(drop=True)
df_new["rank"] = [x + 1 for x in df_new.index]
df_new["winnings"] = df_new["bid"] * df_new["rank"]

# Print solutions
print("Solution to part one:", df["winnings"].sum())
print("Solution to part two:", df_new["winnings"].sum())

# Finalise timer
toc = time.perf_counter()
print(f"Script took {toc - tic:0.2f} seconds to run.")
