import sys
import csv
from typing import List, Tuple
from pathlib import Path
from .datainstance import DataInstance, Attribute


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


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


def read_dataset(file_name: str) -> Tuple[List[DataInstance], List[str]]:
    data_instances = []
    metadata = read_metadata(file_name)

    try:
        with open(file_name) as data_file:
            lines = csv.reader(data_file, delimiter=';')
            headers = next(lines)
            for line in lines:
                target = line[-1]  # get last column
                attribute_values = line[:-1]  # get all but last column
                attributes = create_attributes(headers[:-1], attribute_values, metadata)
                data_instances.append(DataInstance(attributes, target))
        return data_instances, headers
    except FileNotFoundError:
        print('Dataset file not found. Exiting...')
        sys.exit()


def main():
    dataset_file_name = get_file_name()
    data_instances, headers = read_dataset(dataset_file_name)


if __name__ == '__main__':
    main()
