import json
import matplotlib.pyplot as plt
from collections import Counter
import csv
from collections import defaultdict
import pprint


def plot_json_histogram(json_file_path, value_key):
    """
    Parses a JSON file, extracts values for a specified key, and plots a histogram.

    Args:
        json_file_path (str): Path to the JSON file.
        value_key (str): The key within the JSON structure for values to plot.
    """

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    values = []
    text_list = []
    for item in data['conversations']:
        for turn in item['turns']:
            if turn['replay_captured_data']['ReplayCapturedData']['dialog_identifiers']:
                array = turn['replay_captured_data']['ReplayCapturedData']['dialog_identifiers']['array']
                values.append('EMPTY' if not array else array[0])
            else:
                values.append('EMPTY')
            text = turn['ground_truth_information']['asr_post_itn']
            if text:
                text_list.append(text['string'] if text['string'] else 'EMPTY')
            else:
                text_list.append('EMPTY')

    assert len(values) == len(text_list)
    categories = []
    with open('/Users/yima/Downloads/cat_categories.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        rows = list(reader)  # Read the remaining rows

    my_dict = defaultdict(lambda: 'N/A')
    my_dict['EMPTY'] = "EMPTY"
    Not_Found = defaultdict(list)
    Handled = defaultdict(list)
    Empty = defaultdict(list)
    CantDo = defaultdict(list)
    Missing = defaultdict(list)

    for row in rows:
        my_dict[row[0]] = row[1] if row[1] else 'MISSING'
    for index, value in enumerate(values):
        if value not in my_dict:
            Not_Found[value].append(text_list[index])
        elif my_dict[value] == 'HANDLED':
            if value not in Handled:
                Handled[value] = text_list[index]
        elif my_dict[value] == "CAN'T DO":
            if value not in CantDo:
                CantDo[value] = text_list[index]
        elif my_dict[value] == "EMPTY":
            if value not in Empty:
                Empty[value] = text_list[index]
        elif my_dict[value] == "MISSING":
            if value not in Missing:
                Missing[value] = text_list[index]

        categories.append(my_dict[value])

    # print(Not_Found)
    # print(f'Handled: {Handled}')
    # print(f'Cant Do: {CantDo}')
    # print(f'Empty: {Empty}')
    print(f'Missing: {Missing}')

    plot_values_histogram(values, my_dict, value_key)
    plot_values_histogram(categories, my_dict, "cat category")


def plot_values_histogram(values, my_dict, value_key):
    total = len(values)

    # Count occurrences of each value
    value_counts = Counter(values)

    # Sort by count (descending)
    sorted_items = value_counts.most_common()
    # for item in sorted_items[:20]:
    #     print(item[0], item[1], my_dict[item[0]])
    labels, counts = zip(*sorted_items[:50])

    # Create the histogram-like visualization
    plt.hist(labels, bins=len(labels), weights=counts, edgecolor='black')

    # Add text labels on top of each bar
    for i, bar in enumerate(plt.gca().patches):
        value = counts[i]
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height() + 5
        plt.text(x, y, f"{value / total * 100:.1f}%", ha='center', fontsize='x-small')

    plt.xlabel(value_key)
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.xticks(fontsize='x-small')
    plt.tight_layout()
    plt.title(f'Histogram of "{value_key}"')
    plt.show()



# Example usage
json_file_path = '/Users/yima/Downloads/conversational_dataset.avro.json'  # Replace with your JSON file path
value_key = 'dialog_identifiers'  # Replace with the key you want to plot

plot_json_histogram(json_file_path, value_key)
