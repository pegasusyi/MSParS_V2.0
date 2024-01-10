# Function to read file and return a set of lines
def read_file(filename):
    with open(filename, 'r') as file:
        # Read the lines and convert them to a set for efficient searching
        lines = set(file.readlines())
    return lines

# Read the files
lines_in_A = read_file('/Users/yima/Downloads/auto-label.txt')
lines_in_B = read_file('/Users/yima/Downloads/ground_truth.txt')

# Find lines that are in A but not in B
unique_lines_in_A = lines_in_A - lines_in_B

# Count the number of unique lines
unique_count = len(unique_lines_in_A)

# Print the result
print(f'There are {unique_count} lines in A.txt that are not in B.txt.')
