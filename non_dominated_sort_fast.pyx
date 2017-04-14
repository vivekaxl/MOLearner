from __future__ import division
from utility import read_file
from collections import defaultdict
import sys
from itertools import izip

def binary_domination(one, two):
    """
    Binary Domination: We are trying to minimize both SLA and cost
    :param one: First solution
    :param two: Second solution
    :return: True if one dominates two; False otherwise
    """
    not_equal = False
    for o, t in izip(one, two):
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
            # print ". ", dependents[first_count]
            # sys.stdout.flush()
            non_dominated_indexes.append(first_count)

    return non_dominated_indexes

import time
def non_dominated_sort_fast(raw_dependents, lessismore, size = 3):
    # print "# ",len(raw_dependents),
    # start = time.time()
    sys.stdout.flush()
    assert(len(raw_dependents[0]) == len(lessismore)), "Something is wrong"
    dependents = []
    for rd in raw_dependents:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(-1*rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    if len(dependents) < 100:
        # print time.time() - start
        return non_dominated_sort(dependents)

    else:

        chunks = []

        for i in range(0, len(dependents), int(len(dependents)/size)):
            chunks.append(dependents[i:i + int(len(dependents)/size)])

        aggregated_indexes = []
        for i,chunk in enumerate(chunks):
            ret_indexes = non_dominated_sort(chunk)
            for ret_index in ret_indexes:
                aggregated_indexes.append(int(len(dependents)/size) * i + ret_index)

        aggregated_pfs = [dependents[i] for i in aggregated_indexes]
        aggregated_indexes_2 = non_dominated_sort(aggregated_pfs)

        ret_indexes = [aggregated_indexes[i] for i in aggregated_indexes_2]
        # print time.time() - start
        return ret_indexes

if __name__ == "__main__":
    data = read_file("./Data/Sac1_2.csv")
    dependents = [d.objectives for d in data]
    import time
    for size in xrange(1, 20):
        time_holder = []
        for _ in xrange(10):
            print ". ",
            sys.stdout.flush()
            star = time.time()
            pf_indexes = non_dominated_sort_fast(dependents, [False, True], size)
            pf = [dependents[i] for i in pf_indexes]
            pf = sorted(pf, key=lambda x:x[0])
            time_holder.append(time.time() - star)
        print size, sum(time_holder)/len(time_holder)

    # import matplotlib.pyplot as plt
    # plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r')
    # plt.plot([p[0] for p in pf], [p[1] for p in pf], color='green', marker='o')
    # plt.show()
