from abc import ABC, abstractmethod
from datainstance import Attribute, DataInstance


class Node(ABC):
    @abstractmethod
    def classify(self, instance: DataInstance) -> str:
        pass


class LeafNode(Node):
    def __init__(self, classification):
        self._classification = classification

    def classify(self, instance: DataInstance) -> str:
        return self._classification

    def __str__(self) -> str:
        return 'LeafNode{' \
               'classification=' + str(self._classification) + \
               '}'

    def __repr__(self) -> str:
        return str(self)


class DecisionNode(Node):
    def __init__(self, associate_attribute):
        self._associate_attribute = associate_attribute
        self._children_nodes = []

    def add_child(self, attribute_value: str, child_node: Node):
        self._children_nodes.append((attribute_value, child_node))

    def classify(self, instance: DataInstance) -> str:
        for instance_attribute in instance.attributes:
            if instance_attribute.name == self._associate_attribute:
                return self._classify_on_correct_child(instance, instance_attribute)

        raise Exception('Instance does not have the attribute associate with this node. Node attribute: '
                        + self._associate_attribute)

    def _classify_on_correct_child(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        for child_node in self._children_nodes:
            if child_node[0] == instance_attribute.value:
                return child_node[1].classify(instance)

        raise Exception('Attribute value of instance not found on any child node. Attribute value: '
                        + instance_attribute.value + '. Children attribute: ' + self._associate_attribute)

    def __str__(self) -> str:
        return 'DecisionNode{' \
               'associate_attribute=' + str(self._associate_attribute) + \
               ', children_nodes=' + str(self._children_nodes) + \
               '}'

    def __repr__(self) -> str:
        return str(self)
