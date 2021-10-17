import random
from itertools import cycle


def cross_validation_division(dataset, k_folds, r_repetitions, seed=None):
    repetitions = []
    for repetition in range(0, r_repetitions):
        if repetition == 0:
            repetition_offset = 0
        else:
            repetition_offset = get_repetition_offset(dataset, k_folds, seed, repetition)
        print(repetition_offset)
        repetitions.append(fold_division(dataset, k_folds, repetition_offset))
    return repetitions


def get_repetition_offset(dataset, k_folds, seed, repetition):
    num_instances = len(dataset)
    fold_size = int(num_instances / k_folds)
    if seed is not None:
        random.seed(seed + repetition)
    return random.randint(1, fold_size - 1)


def fold_division(dataset, k_folds, repetition_offset):
    num_instances = len(dataset)
    circular_iterator = cycle(dataset)
    fold_size = int(num_instances / k_folds)
    folds = []

    # shift N times, so that folds are different between repetitions
    for i in range(0, repetition_offset):
        next(circular_iterator)

    # create k folds
    for ith_fold in range(0, k_folds):
        fold = []
        for ith_element in range(0, fold_size):
            fold.append(next(circular_iterator))
        folds.append(fold)

    # add remaining instances to last fold when num_instances/k_folds is non-integer,
    # to not lose instances on fold division
    num_remaining_instances = num_instances - (k_folds * fold_size)
    for i in range(0, num_remaining_instances):
        folds[-1].append(next(circular_iterator))

    return folds