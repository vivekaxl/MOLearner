from __future__ import division
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import sys
from random import shuffle
from utility import draw_pareto_front, generational_distance, ranges, inverted_generational_distance


if __name__ == "__main__":
    from utility import read_file, split_data, build_model, lessismore
    from non_dominated_sort_fast import non_dominated_sort_fast
    import os

    # files = ["./Data/" + f for f in os.listdir("./Data/") if ".csv" in f]

    files = [
        "./Data/sort_256.csv",
        "./Data/TriMesh_1_2.csv",
        "./Data/TriMesh_2_3.csv",
        "./Data/wc+rs-3d-c4.csv",
        "./Data/wc+sol-3d-c4.csv",
        "./Data/wc+wc-3d-c4.csv",
        "./Data/wc-3d-c4.csv",
        "./Data/wc-5d-c5.csv",
        "./Data/wc-6d-c1.csv",
        "./Data/wc-c1-3d-c1.csv",
        "./Data/wc-c3-3d-c1.csv",
        "./Data/x264-DB_1_2.csv",
        "./Data/x264-DB_2_3.csv",
        "./Data/x264-DB_3_4.csv",
        "./Data/x264-DB_4_5.csv",
        "./Data/x264-DB_5_6.csv",
        "./Data/xomo_all-p10000-d27-o4-dataset1.csv",
        "./Data/xomo_all-p10000-d27-o4-dataset2.csv",
        "./Data/xomo_all-p10000-d27-o4-dataset3.csv",
        "./Data/xomo_flight-p10000-d27-o4-dataset1.csv",
        "./Data/xomo_flight-p10000-d27-o4-dataset2.csv",
        "./Data/xomo_flight-p10000-d27-o4-dataset3.csv",
        "./Data/xomo_ground-p10000-d27-o4-dataset1.csv",
        "./Data/xomo_ground-p10000-d27-o4-dataset2.csv",
        "./Data/xomo_ground-p10000-d27-o4-dataset3.csv",
        "./Data/xomo_osp-p10000-d27-o4-dataset1.csv",
        "./Data/xomo_osp-p10000-d27-o4-dataset2.csv",
        "./Data/xomo_osp-p10000-d27-o4-dataset3.csv",
        "./Data/xomoo2-p10000-d27-o4-dataset1.csv",
        "./Data/xomoo2-p10000-d27-o4-dataset2.csv",
        "./Data/xomoo2-p10000-d27-o4-dataset3.csv",
    ]

    all_data = {}
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []
        data = read_file(file)
        actual_dependent = [d.objectives for d in data]
        actual_data_pf_indexes = non_dominated_sort_fast(actual_dependent, lessismore[file])
        actual_pf = sorted([actual_dependent[i] for i in actual_data_pf_indexes], key=lambda x: x[0])

        print file
        for _ in xrange(20):
            print ". ",
            sys.stdout.flush()

            shuffle(data)

            selected_data = data[:int(len(data)*0.05)]
            selected_actual_dependent = [d.objectives for d in selected_data]
            selected_data_pf_indexes = non_dominated_sort_fast(selected_actual_dependent, lessismore[file])
            selected_pf = sorted([selected_actual_dependent[i] for i in selected_data_pf_indexes], key=lambda x:x[0])


            # print generational_distance(actual_pf, selected_pf, ranges[file])
            # draw_pareto_front(actual_dependent, actual_pf, sorted(selected_actual_dependent, key=lambda x:x[0]))#, filename=file.split('/')[-1])
            # print "Length of Training set: ", len(temp)
            # print "Length of Validation set: ", len(splits[1])
            # print "Generation Distance: ", generational_distance(true_pf, predicted_pf)
            all_data[file]['evals'].append(len(selected_data))
            all_data[file]['gen_dist'].append(generational_distance(actual_pf, selected_actual_dependent, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(actual_pf, selected_actual_dependent, ranges[file]))
        print

        import pickle
        pickle.dump(all_data[file], open('pop0-based-'+file.split('/')[-1][:-4]+'.p', 'w'))


