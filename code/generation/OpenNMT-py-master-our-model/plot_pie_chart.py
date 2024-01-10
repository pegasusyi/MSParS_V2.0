import sys
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict


def plot_error_type(filename):
    # Create a dictionary to store category counts
    category_counts = defaultdict(int)
    do_not_include = ['Prompt For Clarification', 'Not Ambiguous', 'Chit-chat/Canned']

    # Open and read the file
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() in do_not_include:
                continue
            # Strip newline character and increment count
            category_counts[line.strip()] += 1

    # Prepare data for pie chart
    labels = list(category_counts.keys())
    sizes = list(category_counts.values())

    # Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.show()


def plot_cat_id(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        values = [line.strip() for line in lines]

    # Count the occurrences of each unique value
    counts = Counter(values)

    # Prepare data for the pie chart
    labels = list(counts.keys())
    other_values = [x for x in labels if counts[x] < 1]
    new_values = ['other' if x in other_values else x for x in values]

    new_counts = Counter(new_values)
    new_labels = list(new_counts.keys())
    new_sizes = list(new_counts.values())

    # Plot the pie chart
    plt.pie(new_sizes, labels=new_labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.title("False Trigger Cat Id Distribution", loc="left")
    plt.show()


def plot_cat_id_2(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        values = [line.strip() for line in lines]

    my_dict = {
        'Non English Locale': 'Not An Error',
        'Out of Siri Scope': 'Not An Error',
        'Chit-chat/Canned': 'Not An Error',
        'Nonsensical/Unintelligible': 'Not An Error',
        'More Than One Correct Answer': 'NL and Other Error',
        'More Than 1 Plugin Can Handle': 'NL and Other Error',
        'NL Error': 'NL and Other Error',
        'CAM Error': 'NL and Other Error',
        'Execution Error': 'NL and Other Error',
        'Universal Entity Ambiguity': 'Entity Error',
        'Personal Entity Ambiguity': 'Entity Error'
    }

    my_list = [my_dict[x] if x in list(my_dict.keys()) else x for x in values]

    # Count the occurrences of each unique value
    counts = Counter(my_list)

    # Prepare data for the pie chart
    labels = list(counts.keys())
    sizes = list(counts.values())

    # Plot the pie chart
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.title("False Trigger Cat Id Distribution", loc="left")
    plt.show()


if __name__ == "__main__":
    src_path = sys.argv[1]
    # plot_error_type(src_path)
    plot_cat_id(src_path)
