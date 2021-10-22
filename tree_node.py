from abc import ABC, abstractmethod
from typing import Any, Tuple
from data_instance import Attribute, DataInstance
from constants import LESS_OR_EQUAL, BIGGER_THAN


class Node(ABC):
    @abstractmethod
    def classify(self, instance: DataInstance) -> str:
        pass


class LeafNode(Node):
    def __init__(self, classification: str):
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
    def __init__(self, associate_attribute: str, numeric_attribute_value: float = None):
        self._associate_attribute = associate_attribute
        self._children_nodes = []
        self._numeric_attribute_value = numeric_attribute_value

    def add_child(self, attribute_value: Any, child_node: Node) -> None:
        self._children_nodes.append((attribute_value, child_node))

    def set_as_numeric_node(self, numeric_attribute_value: float) -> None:
        self._numeric_attribute_value = numeric_attribute_value

    def classify(self, instance: DataInstance) -> str:
        for instance_attribute in instance.attributes:
            if instance_attribute.name == self._associate_attribute:
                return self._classify_on_correct_child(instance, instance_attribute)

        raise Exception('Instance does not have the attribute associate with this node. Node attribute: '
                        + self._associate_attribute)

    def _classify_on_correct_child(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        if self._is_node_associate_to_a_numeric_attribute():
            return self._classify_on_numeric_node(instance, instance_attribute)
        else:
            return self._classify_on_categorical_node(instance, instance_attribute)

    def _is_node_associate_to_a_numeric_attribute(self) -> bool:
        return self._numeric_attribute_value is not None

    def _classify_on_numeric_node(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        if float(instance_attribute.value) <= self._numeric_attribute_value:
            correct_node = self._get_numeric_child_with_split_type(LESS_OR_EQUAL)
        else:
            correct_node = self._get_numeric_child_with_split_type(BIGGER_THAN)
        return correct_node[1].classify(instance)

    def _get_numeric_child_with_split_type(self, split_type: str) -> Tuple[str, Node]:
        for child in self._children_nodes:
            if child[0] == split_type:
                return child

        raise Exception('Split type not found on any child node. Split type: ' + split_type)

    def _classify_on_categorical_node(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        for child_node in self._children_nodes:
            if child_node[0] == instance_attribute.value:
                return child_node[1].classify(instance)

        raise Exception('Attribute value of instance not matched on any child node. Attribute value: '
                        + str(instance_attribute.value) + '. Children attribute: ' + self._associate_attribute)

    def __str__(self) -> str:
        return 'DecisionNode{' \
               'associate_attribute=' + str(self._associate_attribute) + \
               ', children_nodes=' + str(self._children_nodes) + \
               '}'

    def __repr__(self) -> str:
        return str(self)
