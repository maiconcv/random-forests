import math
from typing import List
from .datainstance import DataInstance

class EntropyCalculator(object):
    """
    This class handles the entropy calculation for a partition of DataInstances in the tree.
    A new object should be created for each new partition of the tree.
    """
    def __init__(self, data_instances: List[DataInstance]):
        self.DATA_INSTANCES = data_instances
        self.TARGET_INFORMATION_VALUE = self._calculate_entropy_target()
        self.NUM_ATTRIBUTES = len(self.DATA_INSTANCES[0].attributes)
    
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

        for idx in range(self.NUM_ATTRIBUTES):
            info_gain_list.append(self.gain_ID3(idx))

        return info_gain_list.index(max(info_gain_list))

    def _calculate_entropy_target(self) -> float:
        """
        Calculates value of information for the target attribute.
        """
        VALUE_CLASSES = self.__get_target_classes(self.DATA_INSTANCES)
        NUM_DATA_INSTANCES = len(self.DATA_INSTANCES)

        entropy = 0

        for c in VALUE_CLASSES:
            CLASS_DATA_INSTANCES = self.__get_all_data_instances_for_target_class(self.DATA_INSTANCES, c)
            NUM_DATA_INSTANCES_FOR_CLASS = len(CLASS_DATA_INSTANCES)
            entropy -= (NUM_DATA_INSTANCES_FOR_CLASS / NUM_DATA_INSTANCES) \
                    * math.log2(NUM_DATA_INSTANCES_FOR_CLASS / NUM_DATA_INSTANCES)
    
        return entropy
    
    def _calculate_entropy_attribute(self, attr_idx: int) -> float:
        """
        Calculate the entropy for an attribute.
        """
        NUM_DATA_INSTANCES = len(self.DATA_INSTANCES)
        ATTR_CLASSES = self.__get_classes_attribute(attr_idx)
    
        attr_entropy = 0
    
        # Calculate each class entropy
        for c in ATTR_CLASSES:
            CLASS_DATA_INSTANCES = self.__get_all_data_instances_for_class(attr_idx, c)
            NUM_DATA_INSTANCES_FOR_CLASS = len(CLASS_DATA_INSTANCES)
            attr_entropy += (NUM_DATA_INSTANCES_FOR_CLASS / NUM_DATA_INSTANCES) \
                        * self.__calculate_entropy_class(CLASS_DATA_INSTANCES)
        
        return attr_entropy
    
    def __get_classes_attribute(self, attr_idx: int) -> List[str]:
        """
        Retrieves all the different classes of a categorical attribute.
        """
        # Values of the attribute
        attribute_values = []
    
        # Calculate how many in each class
        for d in self.DATA_INSTANCES:
            attribute_values.append(d.attributes[attr_idx].value)
    
        return set(attribute_values)

    def __get_all_data_instances_for_class(self, attr_idx: int, attr_class: str) -> List[DataInstance]:
        """
        Gets all the data instances of a given class.
        """
        return [d for d in self.DATA_INSTANCES if d.attributes[attr_idx].value == attr_class]

    def __get_target_classes(self, data_instances: List[DataInstance]) -> List[str]:
        """
        Get all the different classes for the target attribute.
        """
        # Values of the attribute
        attribute_values = []
    
        # Calculate how many in each class
        for d in data_instances:
            attribute_values.append(d.target)
    
        return set(attribute_values)

    def __get_all_data_instances_for_target_class(self, data_instances: List[DataInstance], target_class: str) -> List[DataInstance]:
        """
        Gets all the data instances for a target value class.
        """
        return [d for d in data_instances if d.target == target_class]
    
    def __calculate_entropy_class(self, data_instances: List[DataInstance]) -> float:
        """
        Calculates the entropy for the data_instances in a given class.
        """
        TARGET_CLASSES = self.__get_target_classes(data_instances)
        NUM_DATA_INSTANCES = len(data_instances)
    
        class_entropy = 0
    
        for c in TARGET_CLASSES:
            CLASS_DATA_INSTANCES = self.__get_all_data_instances_for_target_class(data_instances, c)
            NUM_DATA_INSTANCES_FOR_CLASS = len(CLASS_DATA_INSTANCES)
            class_entropy -= (NUM_DATA_INSTANCES_FOR_CLASS / NUM_DATA_INSTANCES) * \
                        math.log2(NUM_DATA_INSTANCES_FOR_CLASS / NUM_DATA_INSTANCES)
    
        return class_entropy
