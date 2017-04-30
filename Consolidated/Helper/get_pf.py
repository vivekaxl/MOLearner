from __future__ import division
import numpy as np
import os
import sys
from utility import lessismore
from utility import draw_pareto_front, generational_distance, ranges,inverted_generational_distance
import pickle

if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    from non_dominated_sort import non_dominated_sort
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
        all_data[file]['pf'] = []
        print file,
        data = read_file(file)

        actual_dependent = [d.objectives for d in data]
        print len(actual_dependent),
        assert(len(actual_dependent) == len(data)), "Something is wrong"
        true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file])
        true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x:x[0])
        print len(true_pf)

        all_data[file]['pf'] = true_pf
        pickle.dump(all_data, open('./Actual_PF/actual_pf_' + file.split('/')[-1][:-4] + '.p', 'w'))
