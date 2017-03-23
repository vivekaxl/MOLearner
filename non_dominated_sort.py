from __future__ import division
from utility import read_file
from collections import defaultdict
import sys


def binary_domination(one, two):
    """
    Binary Domination: We are trying to minimize both SLA and cost
    :param one: First solution
    :param two: Second solution
    :return: True if one dominates two; False otherwise
    """
    not_equal = False
    for o, t in zip(one, two):
        if o < t:
            not_equal = True
        elif t < o:
            return False
    return not_equal


def non_dominated_sort(dependents):
    non_dominated_indexes = []
    dominating_fits = defaultdict(int)
    for first_count, f_individual in enumerate(dependents):
        for second_count, s_individual in enumerate(dependents):
            if first_count != second_count:
                if binary_domination(f_individual, s_individual) is True:
                    dominating_fits[second_count] += 1
                elif binary_domination(s_individual, f_individual) is True:
                    dominating_fits[first_count] += 1
                    break

        if dominating_fits[first_count] == 0:
            print ". ", dependents[first_count]
            sys.stdout.flush()
            non_dominated_indexes.append(first_count)

    return non_dominated_indexes


if __name__ == "__main__":
    data = read_file("./Data/noc_CM_log.csv")
    dependents = [d.objectives for d in data]
    pf_indexes = non_dominated_sort(dependents)
    pf = [dependents[i] for i in pf_indexes]
    pf = sorted(pf, key=lambda x:x[0])

    import matplotlib.pyplot as plt
    plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r')
    plt.plot([p[0] for p in pf], [p[1] for p in pf], color='black', marker='x')
    plt.show()
