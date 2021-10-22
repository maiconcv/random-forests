from abc import ABC, abstractmethod
from data_instance import Attribute, DataInstance
from constants import LESS_OR_EQUAL, BIGGER_THAN


class Node(ABC):
    @abstractmethod
    def classify(self, instance: DataInstance) -> str:
        pass


class TreeBranch:
    def __init__(self, value: str, node: Node):
        self.value = value
        self.node = node

    def __str__(self) -> str:
        return 'TreeBranch{' \
               'value=' + str(self.value) + \
               ', node=' + str(self.node) + \
               '}'

    def __repr__(self) -> str:
        return str(self)


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
        self._branches = []
        self._numeric_attribute_value = numeric_attribute_value

    def add_branch(self, branch: TreeBranch) -> None:
        self._branches.append(branch)

    def set_as_numeric_node(self, numeric_attribute_value: float) -> None:
        self._numeric_attribute_value = numeric_attribute_value

    def classify(self, instance: DataInstance) -> str:
        for instance_attribute in instance.attributes:
            if instance_attribute.name == self._associate_attribute:
                return self._classify_on_correct_branch(instance, instance_attribute)

        raise Exception('Instance does not have the attribute associate with this node. Node attribute: '
                        + self._associate_attribute)

    def _classify_on_correct_branch(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        if self._is_node_associate_to_a_numeric_attribute():
            return self._classify_on_numeric_node(instance, instance_attribute)
        else:
            return self._classify_on_categorical_node(instance, instance_attribute)

    def _is_node_associate_to_a_numeric_attribute(self) -> bool:
        return self._numeric_attribute_value is not None

    def _classify_on_numeric_node(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        if float(instance_attribute.value) <= self._numeric_attribute_value:
            correct_branch = self._get_numeric_child_branch_with_split_type(LESS_OR_EQUAL)
        else:
            correct_branch = self._get_numeric_child_branch_with_split_type(BIGGER_THAN)
        return correct_branch.node.classify(instance)

    def _get_numeric_child_branch_with_split_type(self, split_type: str) -> TreeBranch:
        for branch in self._branches:
            if branch.value == split_type:
                return branch

        raise Exception('Split type not found on any child branch. Split type: ' + split_type)

    def _classify_on_categorical_node(self, instance: DataInstance, instance_attribute: Attribute) -> str:
        for branch in self._branches:
            if branch.value == instance_attribute.value:
                return branch.node.classify(instance)

        raise Exception('Attribute value of instance not matched on any child branch. Attribute value: '
                        + str(instance_attribute.value) + '. Node attribute: ' + self._associate_attribute)

    def __str__(self) -> str:
        return 'DecisionNode{' \
               'associate_attribute=' + str(self._associate_attribute) + \
               ', branches=' + str(self._branches) + \
               '}'

    def __repr__(self) -> str:
        return str(self)
