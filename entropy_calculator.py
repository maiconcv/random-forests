import math
import operator
import random
from typing import List, Set
from data_instance import DataInstance


class EntropyCalculator(object):
    """
    This class handles the entropy calculation for a partition of DataInstances in the tree.
    A new object should be created for each new partition of the tree.
    """
    def __init__(self, data_instances: List[DataInstance]):
        self.DATA_INSTANCES = data_instances
        self.TARGET_INFORMATION_VALUE = self._calculate_entropy_target()
        NUM_ATTR_TO_CHOOSE =  int(round(math.sqrt(len(self.DATA_INSTANCES[0].attributes))))
        self.SELECTED_ATTRIBUTES = random.choices(range(len(self.DATA_INSTANCES[0].attributes)), k=NUM_ATTR_TO_CHOOSE)
            
    def gain_ID3(self, attr_idx: int) -> float:
        """
        Calculates the information gain for a given data_instances and attribute
        """
        return self.TARGET_INFORMATION_VALUE - self._calculate_entropy_attribute(attr_idx)
    
    def best_attribute(self) -> int:
        """
        Returns the index of attribute with the greatest information gain for the partition.
        """
        info_gain_list = []

        for idx in self.SELECTED_ATTRIBUTES:
            info_gain_list.append(self.gain_ID3(idx))

        return info_gain_list.index(max(info_gain_list))

    def best_numerical_split_point(self, attr_idx: int) -> float:
        """
        Returns the point of best numerical split for the attribute.
        """
        if self.DATA_INSTANCES[0].attributes[attr_idx].is_numeric():
            return self.__get_best_numerical_split(attr_idx)[0]
        else:
            raise Exception("Cannot get best numerical split for categorical attribute")

    def _calculate_entropy_target(self) -> float:
        """
        Calculates value of information for the target attribute.
        """
        value_classes = self.__get_target_classes(self.DATA_INSTANCES)
        num_data_instances = len(self.DATA_INSTANCES)

        entropy = 0

        for c in value_classes:
            class_data_instances = self.__get_all_data_instances_for_target_class(self.DATA_INSTANCES, c)
            num_data_instances_for_class = len(class_data_instances)
            entropy -= (num_data_instances_for_class / num_data_instances) \
                * math.log2(num_data_instances_for_class / num_data_instances)
    
        return entropy
    
    def _calculate_entropy_attribute(self, attr_idx: int) -> float:
        """
        Calculate the entropy for an attribute.
        """
        attr_entropy = 0
        attribute = self.DATA_INSTANCES[0].attributes[attr_idx]
        num_data_instances = len(self.DATA_INSTANCES)

        # Categorical attribute
        if attribute.is_categorical():
            attr_classes = self.__get_classes_categorical_attribute(attr_idx)
                
            # Calculate each class entropy
            for c in attr_classes:
                class_data_instances = self.__get_all_data_instances_for_class(attr_idx, c)
                num_data_instances_for_class = len(class_data_instances)
                attr_entropy += (num_data_instances_for_class / num_data_instances) \
                    * self.__calculate_entropy_class(class_data_instances)
        
        # Numerical attribute
        elif attribute.is_numeric():
            attr_entropy = self.__get_best_numerical_split(attr_idx)[1]

        return attr_entropy
    
    def __get_best_numerical_split(self, attr_idx: int) -> List[float]:
        """
        Return the split_point and entropy with minimum entropy.
        """
        # Get sorted data instances to evaluate target value boundaries
        sorted_data_instances = sorted(self.DATA_INSTANCES, key=lambda x: x.attributes[attr_idx].value)
        num_data_instances = len(sorted_data_instances)

        # Possible split points
        possible_splits = []

        # Find possible splits
        for i in range(1, len(sorted_data_instances)):
            # If in boundary
            prev = sorted_data_instances[i - 1]
            curr = sorted_data_instances[i]
            if prev.target.value != curr.target.value:
                # Create split point
                possible_splits.append((float(prev.attributes[attr_idx].value) +
                                        float(curr.attributes[attr_idx].value)) / 2)

        splits_entropy = {}

        # Calculate the entropy for each possible split
        for split in possible_splits:
            leq_instances, g_instances = self.__get_all_data_instances_for_numerical_class(attr_idx, split)

            split_entropy = 0
            # Calculate each class entropy
            for SPLIT_INSTANCES in [leq_instances, g_instances]:
                num_data_instances_for_class = len(SPLIT_INSTANCES)
                split_entropy += (num_data_instances_for_class / num_data_instances) \
                    * self.__calculate_entropy_class(SPLIT_INSTANCES)
    
            splits_entropy[split] = split_entropy

        return min(splits_entropy.items(), key=operator.itemgetter(1))

    def __get_classes_categorical_attribute(self, attr_idx: int) -> Set[str]:
        """
        Retrieves all the different classes of an attribute.
        """
        return set([d.attributes[attr_idx].value for d in self.DATA_INSTANCES])

    def __get_all_data_instances_for_numerical_class(self, attr_idx: int, split_point: float) -> List[List[DataInstance]]:
        """
        Return the splitted data instances for a given split point.
        """
        leq_instances = [d for d in self.DATA_INSTANCES if float(d.attributes[attr_idx].value) <= split_point]
        g_instances = [d for d in self.DATA_INSTANCES if float(d.attributes[attr_idx].value) > split_point]

        return [leq_instances, g_instances]

    def __get_all_data_instances_for_class(self, attr_idx: int, attr_class: str) -> List[DataInstance]:
        """
        Gets all the data instances of a given class.
        """
        return [d for d in self.DATA_INSTANCES if d.attributes[attr_idx].value == attr_class]

    def __get_target_classes(self, data_instances: List[DataInstance]) -> Set[str]:
        """
        Get all the different classes for the target attribute.
        """
        # Values of the attribute
        attribute_values = []
    
        # Calculate how many in each class
        for d in data_instances:
            attribute_values.append(d.target.value)
    
        return set(attribute_values)

    def __get_all_data_instances_for_target_class(self, data_instances: List[DataInstance], target_class: str) -> List[DataInstance]:
        """
        Gets all the data instances for a target value class.
        """
        return [d for d in data_instances if d.target.value == target_class]

    def __calculate_entropy_class(self, data_instances: List[DataInstance]) -> float:
        """
        Calculates the entropy for the data_instances in a given class.
        """
        target_classes = self.__get_target_classes(data_instances)
        num_data_instances = len(data_instances)
    
        class_entropy = 0
    
        for c in target_classes:
            class_data_instances = self.__get_all_data_instances_for_target_class(data_instances, c)
            num_data_instances_for_class = len(class_data_instances)
            class_entropy -= (num_data_instances_for_class / num_data_instances) * \
                math.log2(num_data_instances_for_class / num_data_instances)
    
        return class_entropy
