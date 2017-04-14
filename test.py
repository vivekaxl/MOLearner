from utility import read_file
from non_dominated_sort_fast import non_dominated_sort_fast
import sys

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