from __future__ import division
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import sys
from random import shuffle
from utility import draw_pareto_front, generational_distance, ranges, inverted_generational_distance


if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    from non_dominated_sort import non_dominated_sort

    files = ['./Data/llvm_input.csv', './Data/noc_CM_log.csv',
             './Data/rs-6d-c3.csv', './Data/sort_256.csv',
             './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
             './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
             './Data/wc-c3-3d-c1.csv']

    lessismore = {}
    lessismore['./Data/llvm_input.csv'] = [False, False]
    lessismore['./Data/noc_CM_log.csv'] = [False, False]
    lessismore['./Data/sort_256.csv'] = [False, False]
    lessismore['./Data/rs-6d-c3.csv'] = [False, True]
    lessismore['./Data/wc+rs-3d-c4.csv'] = [False, True]
    lessismore['./Data/wc+sol-3d-c4.csv'] = [False, True]
    lessismore['./Data/wc+wc-3d-c4.csv'] = [False, True]
    lessismore['./Data/wc-3d-c4.csv'] = [False, True]
    lessismore['./Data/wc-5d-c5.csv'] = [False, True]
    lessismore['./Data/wc-6d-c1.csv'] = [False, True]
    lessismore['./Data/wc-c1-3d-c1.csv'] = [False, True]
    lessismore['./Data/wc-c3-3d-c1.csv'] = [False, True]

    all_data = {}
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []

        print file
        for _ in xrange(40):
            print ". ",
            sys.stdout.flush()
            data = read_file(file)
            shuffle(data)

            selected_data = data[:int(len(data)*0.05)]
            selected_actual_dependent = [d.objectives for d in selected_data]
            selected_data_pf_indexes = non_dominated_sort(selected_actual_dependent, lessismore[file])
            selected_pf = sorted([selected_actual_dependent[i] for i in selected_data_pf_indexes], key=lambda x:x[0])

            actual_dependent = [d.objectives for d in data]
            actual_data_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])
            actual_pf = sorted([actual_dependent[i] for i in actual_data_pf_indexes], key=lambda x:x[0])


            # print generational_distance(actual_pf, selected_pf, ranges[file])
            # draw_pareto_front(actual_dependent, actual_pf, sorted(selected_actual_dependent, key=lambda x:x[0]))#, filename=file.split('/')[-1])
            # print "Length of Training set: ", len(temp)
            # print "Length of Validation set: ", len(splits[1])
            # print "Generation Distance: ", generational_distance(true_pf, predicted_pf)
            all_data[file]['evals'].append(len(selected_data))
            all_data[file]['gen_dist'].append(generational_distance(actual_pf, selected_actual_dependent, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(actual_pf, selected_actual_dependent, ranges[file]))
        print

        print [round(x, 5) for x in all_data[file]['evals']]
        print [round(x, 5) for x in all_data[file]['gen_dist']]
        print [round(x, 5) for x in all_data[file]['igd']]

    import pickle
    pickle.dump(all_data, open('pop0-based.p', 'w'))


