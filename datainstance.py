from typing import List


class DataInstance:
    def __init__(self, attributes: List[str], target: str):
        self.attributes = attributes
        self.target = target

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return 'DataInstance{' \
               'attributes=' + str(self.attributes) + \
               ', target=' + str(self.target) + \
               '}'
