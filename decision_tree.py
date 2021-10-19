from copy import deepcopy
from typing import List, Tuple, Dict
from data_instance import DataInstance
from entropy_calculator import EntropyCalculator
from tree_node import Node, LeafNode, DecisionNode


def get_decision_tree(data_instances: List[DataInstance],
                      attributes: List[str],
                      possible_values_for_each_attribute: Dict[str, List[str]]) -> Node:
    if instances_have_the_same_target(data_instances):
        return LeafNode(data_instances[0].target.value)

    if len(attributes) == 0:
        return LeafNode(most_frequent_target_of(data_instances))

    entropy_calculator = EntropyCalculator(data_instances)
    attribute_index_with_best_division_criteria = entropy_calculator.best_attribute()
    node = DecisionNode(data_instances[0].attributes[attribute_index_with_best_division_criteria].name)
    available_attributes = deepcopy(attributes)
    attribute_name = available_attributes[attribute_index_with_best_division_criteria]
    available_attributes.remove(attribute_name)

    attribute_index = attribute_index_with_best_division_criteria
    if data_instances[0].attributes[attribute_index].attr_type == 'c':
        for attribute_value in possible_values_for_each_attribute[attribute_name]:
            new_possible_instances = instances_with_attribute_value(attribute_value, attribute_name, data_instances)
            if len(new_possible_instances) == 0:
                return LeafNode(most_frequent_target_of(data_instances))
            else:
                instances_without_attribute = remove_attribute_from_instances(new_possible_instances, attribute_index)
                new_node = get_decision_tree(instances_without_attribute, available_attributes, possible_values_for_each_attribute)
                node.add_child(attribute_value, new_node)
        return node
    else:  # numeric
        for split_type_split_point in possible_values_from_numeric_attribute(attribute_index, entropy_calculator):
            attribute_value = split_type_split_point[1]
            split_type = split_type_split_point[0]
            new_possible_instances = instances_that_are_at_range_of(attribute_value, attribute_name, split_type, data_instances)
            if len(new_possible_instances) == 0:
                return LeafNode(most_frequent_target_of(data_instances))
            else:
                node.set_as_numeric_node(attribute_value)
                instances_without_attribute = remove_attribute_from_instances(new_possible_instances, attribute_index)
                new_node = get_decision_tree(instances_without_attribute, available_attributes, possible_values_for_each_attribute)
                node.add_child(split_type, new_node)
        return node


def instances_have_the_same_target(instances: List[DataInstance]) -> bool:
    first_target = instances[0].target.value

    for instance in instances:
        if instance.target.value != first_target:
            return False
    return True


def most_frequent_target_of(data_instances: List[DataInstance]) -> str:
    # get the target of all instances
    targets = []
    for instance in data_instances:
        targets.append(instance.target)

    # get the unique targets
    unique_targets = set(targets)

    # calculate how many times a target appears
    target_quantity = {}
    for target in unique_targets:
        target_quantity[target] = targets.count(target)

    # calculate the most frequent target
    most_frequent_target = None
    quantity_of_most_frequent_target = -1
    for target in target_quantity:
        if target_quantity[target] > quantity_of_most_frequent_target:
            most_frequent_target = target
            quantity_of_most_frequent_target = target_quantity[target]
    return most_frequent_target.value


def possible_values_of_attribute(attribute_name: str, data_instances: List[DataInstance]) -> List[str]:
    attribute_values = []
    for instance in data_instances:
        attribute_values.append(instance.attribute_with_name(attribute_name).value)

    return list(set(attribute_values))


def instances_with_attribute_value(
        attribute_value: str, attribute_name: str, data_instances: List[DataInstance]) -> List[DataInstance]:
    return [instance for instance in data_instances
            if instance.attribute_with_name(attribute_name).value == attribute_value]


def remove_attribute_from_instances(data_instances: List[DataInstance], attribute_index: int) -> List[DataInstance]:
    instances_without_attribute = []
    for instance in data_instances:
        new_attributes = deepcopy(instance.attributes)
        new_attributes.pop(attribute_index)
        new_attributes.append(instance.target)
        instances_without_attribute.append(DataInstance(instance.id, new_attributes))
    return instances_without_attribute


def instances_that_are_at_range_of(attribute_value: float,
                                   attribute_name: str,
                                   split_type: str,
                                   data_instances: List[DataInstance]) -> List[DataInstance]:
    new_instances = []
    for instance in data_instances:
        if split_type == 'LE' and float(instance.attribute_with_name(attribute_name).value) <= attribute_value:
            new_instances.append(instance)
        elif split_type == 'BT' and float(instance.attribute_with_name(attribute_name).value) > attribute_value:
            new_instances.append(instance)
    return new_instances


def possible_values_from_numeric_attribute(attribute_index: int,
                                           entropy_calculator: EntropyCalculator) -> List[Tuple[str, float]]:
    split_point = entropy_calculator.best_numerical_split_point(attribute_index)
    return [
        ('LE', split_point),
        ('BT', split_point)
    ]
