from typing import List

class Attribute(object):
    def __init__(self, name: str, value: str, attr_type: str):
        self.name = name
        self.attr_type = attr_type
        if (self.attr_type == 'c'):
            self.value = value
        elif self.attr_type == 'n':
            self.value = float(value)
        else:
            raise Exception("Invalid metadata type")

    def __str__(self) -> str:
        return "Attribute(" \
            "name=" + self.name + \
            ", value=" + str(self.value) + \
            ", type=" + self.attr_type + \
            "}" 

    def __repr__(self) -> str:
        return str(self)


class DataInstance:
    def __init__(self, attributes: List[Attribute], target: str):
        self.attributes = attributes
        self.target = target

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return 'DataInstance{' \
               'attributes=' + str(self.attributes) + \
               ', target=' + str(self.target) + \
               '}'
