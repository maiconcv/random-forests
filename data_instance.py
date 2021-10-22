from typing import List
from constants import CATEGORICAL, NUMERIC, TARGET


class Attribute(object):
    def __init__(self, name: str, value: str, attr_type: str):
        self.name = name
        self.attr_type = attr_type
        if self.is_categorical() or self.is_target():
            self.value = value
        elif self.is_numeric():
            self.value = float(value)
        else:
            raise Exception('Invalid metadata type')

    def is_categorical(self):
        return self.attr_type == CATEGORICAL

    def is_numeric(self):
        return self.attr_type == NUMERIC

    def is_target(self):
        return self.attr_type == TARGET

    def __str__(self) -> str:
        return 'Attribute{' \
            'name=' + self.name + \
            ', value=' + str(self.value) + \
            ', type=' + self.attr_type + \
            '}'

    def __repr__(self) -> str:
        return str(self)
        

class DataInstance:
    def __init__(self, instance_id: int, attributes: List[Attribute]):
        self.id = instance_id
        # Get index of target attribute
        target_attr = attributes.pop(
            attributes.index(next(attribute for attribute in attributes if attribute.is_target())))
        self.attributes = attributes
        self.target = target_attr

    def attribute_with_name(self, attribute_name: str) -> Attribute:
        for attribute in self.attributes:
            if attribute.name == attribute_name:
                return attribute

        raise Exception('Attribute not found in data instance. Attribute name: ' + attribute_name)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return 'DataInstance{' \
               'id=' + str(self.id) + \
               ', attributes=' + str(self.attributes) + \
               ', target=' + str(self.target) + \
               '}'

    def __eq__(self, obj):
        return self.id == obj.id
