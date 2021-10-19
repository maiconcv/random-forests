import sys
import csv
from typing import List, Tuple, Dict
from pathlib import Path
from data_instance import DataInstance, Attribute
from decision_tree import get_decision_tree


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
        if metadata[idx] == 't':
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


def possible_values_of_attributes(data_instances: List[DataInstance]) -> Dict[str, List[str]]:
    possible_values = {}

    # initialize every attribute with an empty list inside dictionary
    for attribute in data_instances[0].attributes:
        possible_values[attribute.name] = []

    # append every attribute value of every instance into the list inside dictionary
    for instance in data_instances:
        for attribute in instance.attributes:
            possible_values[attribute.name].append(attribute.value)

    # transform every attribute list inside dictionary into an unique list
    for attribute in possible_values:
        possible_values[attribute] = list(set(possible_values[attribute]))

    return possible_values


def main():
    dataset_file_name = get_file_name()
    data_instances, headers = read_dataset(dataset_file_name, delimiter='\t')
    all_values_of_attributes = possible_values_of_attributes(data_instances)
    node = get_decision_tree(data_instances, headers, all_values_of_attributes)
    print(node)

    classification = {
        True: 0,
        False: 0
    }

    for test_instance in data_instances:
        classification_result = node.classify(test_instance)
        classification[classification_result == test_instance.target.value] += 1
    print(classification)


if __name__ == '__main__':
    main()
