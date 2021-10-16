import random
from copy import deepcopy


class Bootstrap:
    def __init__(self, training_set, test_set):
        self.training_set = training_set
        self.test_set = test_set

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return 'Bootstrap{' \
               'training_set=' + str(self.training_set) + \
               ', test_set=' + str(self.test_set) + \
               '}'


def bootstraps_with_resampling(dataset, b_bootstraps, seed=None):
    bootstraps = []
    for bootstrap_index in range(0, b_bootstraps):
        bootstraps.append(create_bootstrap(dataset, bootstrap_index, seed))
    return bootstraps


def create_bootstrap(dataset, bootstrap_index, seed):
    num_instances = len(dataset)
    training_set = []
    test_set = []

    if seed is not None:
        random.seed(seed + bootstrap_index)

    # divide dataset into training and test sets, with each instance having 80% of being a training instance
    for instance in range(0, num_instances):
        training_chance = random.randint(0, 99)
        if training_chance < 80:
            training_set.append(dataset[instance])
        else:
            test_set.append(dataset[instance])

    # resample training set until its size is equal to original dataset size
    training_set_original_size = len(training_set)
    num_instances_to_resample = num_instances - training_set_original_size
    for num in range(0, num_instances_to_resample):
        resampled_instance_index = random.randint(0, training_set_original_size - 1)
        resampled_instance = training_set[resampled_instance_index]
        training_set.append(deepcopy(resampled_instance))

    return Bootstrap(training_set, test_set)
