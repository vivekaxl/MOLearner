from __future__ import division
from utility import read_file, lessismore, generational_distance, ranges
from non_dominated_sort import non_dominated_sort

"""
    This function would find the worst possible frontier a search algorithm can achieve.
    This can be found out of inverting the goals of the objectives. For example, if there
    are two objectives in a problem. Both of these objectives are to be maximized. We can invert
    the objectives to minimized and find the true frontier. This would help us to find the
     best generational distance and worst possible generational distance. This way we can represent
     the GD score can be normalized to the worst possible value.
"""


def find_worst_possible_distance(filename):
    data = read_file(filename)
    minmax = lessismore[filename]
    invminmax = [not item for item in minmax]
    training_indep = [r.decisions for r in data]
    training_dep = [r.objectives for r in data]
    assert(len(data) == len(training_dep)), "Something is wrong"

    # Find Non-Dominated Solutions
    invpf_indexes = non_dominated_sort(training_dep, invminmax)
    invpf = [training_dep[i] for i in invpf_indexes]

    pf_indexes = non_dominated_sort(training_dep, minmax)
    pf = [training_dep[i] for i in pf_indexes]

    worst_possible = generational_distance(pf, invpf, ranges[filename])

    print filename, worst_possible



if __name__ == "__main__":
    files = ['./Data/llvm_input.csv', './Data/noc_CM_log.csv',
              './Data/sort_256.csv',
             './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
             './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
             './Data/wc-c3-3d-c1.csv', './Data/rs-6d-c3.csv']

    for file in files:
        find_worst_possible_distance(file)