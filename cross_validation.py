import random
from itertools import cycle
from typing import List, Dict
from collections import Counter
from data_instance import DataInstance


def cross_validation_division(dataset: List[DataInstance], k_folds: int, r_repetitions: int, seed=None):
    repetitions = []
    for repetition in range(r_repetitions):
        if repetition == 0:
            repetition_offset = 0
        else:
            repetition_offset = _get_repetition_offset(dataset, k_folds, seed, repetition)
        repetitions.append(_fold_division(dataset, k_folds, repetition_offset))
    return repetitions


def _get_repetition_offset(dataset, k_folds, seed, repetition):
    num_instances = len(dataset)
    fold_size = int(num_instances / k_folds)
    if seed is not None:
        random.seed(seed + repetition)
    return random.randint(1, fold_size - 1)


def _fold_division(dataset, k_folds, repetition_offset):
    strata_distribution = _get_strata_distribution(dataset)
    num_instances = len(dataset)
    circular_iterator = cycle(dataset)
    fold_size = int(num_instances / k_folds)
    folds = []

    # shift N times, so that folds are different between repetitions
    for i in range(repetition_offset):
        next(circular_iterator)

    # create k folds
    for ith_fold in range(k_folds):
        fold = []
        for strata in strata_distribution.keys():
            strata_size = int(round(strata_distribution[strata] * fold_size))
            for ith_element in range(strata_size):
                el = next(circular_iterator)
                
                while el.target.value != strata:
                    el = next(circular_iterator)    
                
                fold.append(el)

        folds.append(fold)

    # add remaining instances to last fold when num_instances/k_folds is non-integer,
    # to not lose instances on fold division
    num_remaining_instances = num_instances - (k_folds * fold_size)
    for i in range(num_remaining_instances):
        folds[-1].append(next(circular_iterator))

    return folds

def _get_strata_distribution(dataset: List[DataInstance]) -> Dict[str, float]:
    NUM_INSTANCES = len(dataset)
    OCCURRENCES = Counter([d.target.value for d in dataset])

    strata_distribution = {}
    for o in OCCURRENCES:
        strata_distribution[o] = OCCURRENCES[o] / NUM_INSTANCES

    return strata_distribution