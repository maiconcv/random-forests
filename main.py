import sys
import csv
from typing import List, Tuple
from datainstance import DataInstance


def get_file_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Missing dataset file argument. Exiting...')
        sys.exit()


def read_dataset(file_name: str) -> Tuple[List[DataInstance], List[str]]:
    data_instances = []
    try:
        with open(file_name) as data_file:
            lines = csv.reader(data_file, delimiter=';')
            headers = next(lines)
            for line in lines:
                target = line[-1]  # get last column
                attributes = line[:-1]  # get all but last column
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
