import sys
import csv
import statistics
import os
from typing import List, Tuple
from pathlib import Path
from data_instance import DataInstance, Attribute
from random_forest import RandomForest
from cross_validation import cross_validation_division
from constants import TARGET


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


def get_data_headers(headers: List[str], metadata: List[str]) -> List[str]:
    """
    Remove the target attribute from the headers leaving only the data attributes.
    """
    assert len(headers) == len(metadata)

    new_headers = headers

    for idx in range(len(new_headers)):
        if metadata[idx] == TARGET:
            del new_headers[idx]
            break

    return new_headers


def read_metadata(file_path: str) -> List[str]:
    """
    Reads the metadata file associated with data.
    Metadata files are files with only one csv line.
    It is expected that metadata file names are just the db file name with _metadata appended to it.
    """
    try:
        p = Path(file_path)
        p = p.with_name(p.stem + "_metadata.csv")
        with open(p) as f:
            reader = csv.reader(f, delimiter=",")
            metadata = next(reader)

        return metadata
    except FileNotFoundError:
        print("Dataset metadata file not found. Exiting...")
        sys.exit()


def create_attributes(header: List[str], attribute_values: List[str], attributes_metadata: List[str]) -> List[Attribute]:
    """
    Create a list of attribute objects based on the header, values and type metadata.
    """
    attributes = []

    # For each attribute
    for idx in range(len(header)):
        attributes.append(Attribute(header[idx], attribute_values[idx], attributes_metadata[idx]))

    return attributes


def read_dataset(file_name: str, delimiter: str = ';') -> Tuple[List[DataInstance], List[str]]:
    data_instances = []
    metadata = read_metadata(file_name)

    try:
        with open(file_name) as data_file:
            lines = csv.reader(data_file, delimiter=delimiter)
            headers = next(lines)
            instance_index = 0
            for line in lines:
                attribute_values = line  # get all but last column
                attributes = create_attributes(headers, attribute_values, metadata)
                data_instances.append(DataInstance(instance_index, attributes))
                instance_index += 1
            
            headers = get_data_headers(headers, metadata)
        
        return data_instances, headers
    except FileNotFoundError:
        print('Dataset file not found. Exiting...')
        sys.exit()


def run_cross_validation(folds: List[DataInstance], headers: List[str], num_trees: int):
    NUM_FOLDS = len(folds)

    test_fold = 0
    accuracy_list = []

    for i in range(NUM_FOLDS):
        training_set = [data for i in range(NUM_FOLDS) if i != test_fold for data in folds[i]]
        forest = RandomForest(training_set, num_trees, headers)
        # Evaluate performance of forest
        pred = forest.classify(folds[test_fold])
        accuracy_list.append(count_equal_elements(pred, [d.target.value for d in folds[test_fold]]) / len(pred))
        test_fold += 1

    return statistics.mean(accuracy_list), statistics.stdev(accuracy_list)


def count_equal_elements(pred, real):
    assert len(pred) == len(real)

    count = 0

    for i in range(len(pred)):
        if pred[i] == real[i]:
            count += 1

    return count


def main():
    dataset_file_name = get_file_name()
    data_instances, headers = read_dataset(dataset_file_name, delimiter='\t')
    [folds] = cross_validation_division(data_instances, int(sys.argv[2]), 1)
    mean, stdev = run_cross_validation(folds, headers, int(sys.argv[3]))
    print("Accuracy Mean: {0:.3f}%, Standard Dev: {1:.3f}%".format(mean*100, stdev*100))


def generate_data():
    datasets_to_run = []
    for f in os.listdir("./dataset"):
        if f.endswith(".tsv"):
            datasets_to_run.append(Path(os.path.join("./dataset", f)))

    NUM_FOLDS = [3, 5, 7, 10]
    NUM_TREES = [1, 5, 10, 25, 50, 75, 100]

    if not os.path.exists('./results'):
        os.mkdir('./results/')

    for d in datasets_to_run:
        # CSV with results
        csv_rows = [['k_folds', 'num_trees', 'mean', 'stdev']]
        with open("./results/" + d.stem + ".csv", 'w') as csv_file:
            data_instances, headers = read_dataset(d, delimiter='\t')
            for f in NUM_FOLDS:
                [folds] = cross_validation_division(data_instances, f, 1)
                for t in NUM_TREES:
                    mean, stdev = run_cross_validation(folds, headers, t)
                    csv_rows.append([f, t, mean, stdev])
                    # Throw to csv
                    print("Folds {2} Trees {3} - Accuracy Mean: {0:.3f}%, Standard Dev: {1:.3f}%".format(mean*100, stdev*100, f, t))

            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)


if __name__ == '__main__':
    generate_data()
