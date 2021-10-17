from copy import deepcopy
from typing import List
from datainstance import DataInstance
from entropy_calculator import EntropyCalculator
from tree_node import Node, LeafNode, DecisionNode


def get_decision_tree(data_instances: List[DataInstance], attributes: List[str]) -> Node:
    if instances_have_the_same_target(data_instances):
        return LeafNode(data_instances[0].target)

    if len(attributes) == 0:
        return LeafNode(most_frequent_target_of(data_instances))

    attribute_index_with_best_division_criteria = EntropyCalculator(data_instances).best_attribute()
    node = DecisionNode(data_instances[0].attributes[attribute_index_with_best_division_criteria].name)
    available_attributes = deepcopy(attributes)
    available_attributes.remove(available_attributes[attribute_index_with_best_division_criteria])

    attribute_index = attribute_index_with_best_division_criteria
    for attribute_value in possible_values_of_attribute(attribute_index, data_instances):
        new_possible_instances = instances_with_attribute_value(attribute_value, attribute_index, data_instances)
        if len(new_possible_instances) == 0:
            return LeafNode(most_frequent_target_of(data_instances))
        else:
            instances_without_attribute = remove_attribute_from_instances(new_possible_instances, attribute_index)
            new_node = get_decision_tree(instances_without_attribute, available_attributes)
            node.add_child(attribute_value, new_node)
    return node


def instances_have_the_same_target(instances: List[DataInstance]) -> bool:
    first_target = instances[0].target

    for instance in instances:
        if instance.target != first_target:
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
    return most_frequent_target


def possible_values_of_attribute(attribute_index: int, data_instances: List[DataInstance]) -> List[str]:
    attribute_values = []
    for instance in data_instances:
        attribute_values.append(instance.attributes[attribute_index].value)

    return list(set(attribute_values))


def instances_with_attribute_value(
        attribute_value: str, attribute_index: int, data_instances: List[DataInstance]) -> List[DataInstance]:
    return [instance for instance in data_instances if instance.attributes[attribute_index].value == attribute_value]


def remove_attribute_from_instances(data_instances: List[DataInstance], attribute_index: int) -> List[DataInstance]:
    instances_without_attribute = []
    for instance in data_instances:
        new_attributes = deepcopy(instance.attributes)
        new_attributes.pop(attribute_index)
        instances_without_attribute.append(DataInstance(new_attributes, instance.target))
    return instances_without_attribute
