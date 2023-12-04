# Import modules
import os


# Function to get line-by-line strings from a .txt file
def get_line_strings(relative_input_filepath):
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_filepath = os.path.join(parent_directory, relative_input_filepath)
    input_file = open(input_filepath, "r")
    input = input_file.readlines()
    input_file.close
    return input
