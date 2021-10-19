from typing import List


class Attribute(object):
    def __init__(self, name: str, value: str, attr_type: str):
        self.name = name
        self.attr_type = attr_type
        if self.attr_type == 'c':
            self.value = value
        elif self.attr_type == 'n':
            self.value = float(value)
        elif self.attr_type == 't':
            self.value = value
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
    def __init__(self, instance_id: int, attributes: List[Attribute]):
        self.id = instance_id
        # Get index of target attribute
        target_attr = attributes.pop(
            attributes.index(next(a for a in attributes if a.attr_type == 't')))
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
               'attributes=' + str(self.attributes) + \
               ', target=' + str(self.target) + \
               '}'
