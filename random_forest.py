from collections import Counter
from decision_tree import get_decision_tree, possible_values_of_attributes
from bootstrap import *


class RandomForest(object):
    def __init__(self, dataset: List[DataInstance], num_trees: int, data_headers: List[str]):
        self.DATASET = dataset
        self.NUM_TREES = num_trees
        self.DATA_HEADERS = data_headers
        # Get bootstraps
        self.BOOTSTRAPS = bootstraps_with_resampling(self.DATASET, self.NUM_TREES)
        # Create trees
        self.TREES = [get_decision_tree(b.training_set, self.DATA_HEADERS, possible_values_of_attributes(self.DATASET)) for b in self.BOOTSTRAPS]
    
    def classify(self, test_set: List[DataInstance]) -> str:
        """
        Majority vote classification for Random Forest.
        """
        pred = [self.__most_common([t.classify(data) for t in self.TREES]) for data in test_set]        

        return pred 

    def __most_common(self, l: List[object]):
        data = Counter(l)
        return data.most_common(1)[0][0]
