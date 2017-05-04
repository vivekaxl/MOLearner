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

    files = [
        '../../Data/llvm_input.csv',
        '../../Data/noc_CM_log.csv',
        '../../Data/sort_256.csv',
        '../../Data/wc+rs-3d-c4.csv',
        '../../Data/wc+sol-3d-c4.csv',
        '../../Data/wc+wc-3d-c4.csv',
        '../../Data/wc-3d-c4.csv',
        '../../Data/wc-5d-c5.csv',
        '../../Data/wc-6d-c1.csv',
        '../../Data/wc-c1-3d-c1.csv',
        '../../Data/wc-c3-3d-c1.csv',
        '../../Data/rs-6d-c3.csv',
        '../../Data/MONRP_50_4_5_0_110.csv',
        '../../Data/MONRP_50_4_5_0_90.csv',
        '../../Data/MONRP_50_4_5_4_110.csv',
        '../../Data/MONRP_50_4_5_4_90.csv',
        '../../Data/POM3A.csv',
        '../../Data/POM3B.csv',
        '../../Data/POM3C.csv',
        '../../Data/POM3D.csv',
        '../../Data/xomo_all.csv',
        '../../Data/xomo_flight.csv',
        '../../Data/xomo_ground.csv',
        '../../Data/xomo_osp.csv',
        '../../Data/xomoo2.csv'
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
        pickle.dump(all_data, open('./ActualPF/actual_pf_' + file.split('/')[-1][:-4] + '.p', 'w'))
