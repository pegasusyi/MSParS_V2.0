import sys
import csv


def split_data(filename, train=0.8, validate=0.1, test=0.1):
    # Checking if the split ratios sum up to 1
    if int(train + validate + test) != 1:
        raise ValueError('Invalid split ratios. Please make sure they sum up to 1.')

    with open(filename, 'r') as csv_file:
        data = list(csv.reader(csv_file, delimiter=',', quotechar='"'))

    train_index = int(len(data) * train)
    validate_index = int(len(data) * (train + validate))

    train_data = data[:train_index]
    validate_data = data[train_index:validate_index]
    test_data = data[validate_index:]

    result = filename.rsplit('.', maxsplit=1)
    train_path = result[0] + '-train.' + result[1]
    dev_path = result[0] + '-dev.' + result[1]
    test_path = result[0] + '-test.' + result[1]

    # Write data to files
    with open(train_path, 'w', newline='') as train_file:
        writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(train_data)

    with open(dev_path, 'w', newline='') as validate_file:
        writer = csv.writer(validate_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(train_data[0])
        writer.writerows(validate_data)

    with open(test_path, 'w', newline='') as test_file:
        writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(train_data[0])
        writer.writerows(test_data)


if __name__ == "__main__":
    csv_path = sys.argv[1]
    split_data(csv_path)
