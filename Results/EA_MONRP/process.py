from __future__ import division
import pickle
import os
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import generational_distance, inverted_generational_distance
import pickle

ranges = {}
ranges['./Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.csv'] = [[97149.0,98385.0],[448.0,708.0]]
ranges['./Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.csv'] = [[448.0,708.0],[99396.0,99635.0]]
ranges['./Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.csv'] = [[96178.0,97619.0],[424.0,639.0]]
ranges['./Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.csv'] = [[424.0,639.0],[99436.0,99626.0]]
ranges['./Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.csv'] = [[95538.0,97364.0],[472.0,727.0]]
ranges['./Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.csv'] = [[472.0,727.0],[99368.0,99603.0]]
ranges['./Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.csv'] = [[94860.0,96797.0],[410.0,621.0]]
ranges['./Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.csv'] = [[410.0,621.0],[99419.0,99619.0]]


actual_pf_p = "./ActualPF/consolidated_dict.p"
folder = "./Data/"
subfolders = [folder + f + "/" for f in os.listdir(folder) if ".DS_Store" not in f]

all_data = {}



for subfolder in subfolders:
    repeats = [subfolder + f + "/" for f in os.listdir(subfolder) if ".DS_Store" not in f]
    print subfolder
    if "SWAY5" not in subfolder: continue

    if "NSGAII" in subfolder or "SPEA2" in subfolder:
        # Find appropriate file
        problem_name_1 = "_".join(subfolder.split('/')[-2].replace('-', '_').split('_')[1:7])
        problem_name_2 = "_".join(subfolder.split('/')[-2].replace('-', '_').split('_')[7:9])
        if problem_name_2 == "1_2":
            problem_name_2 = "dataset1"
        if problem_name_2 == "2_3":
            problem_name_2 = "dataset2"

    elif "SWAY5" in subfolder:
        # Find appropriate file
        problem_name_1 = "_".join(subfolder.split('/')[-2].replace('SWAY5_', '').replace("-", "_").split("_")[:6])
        problem_name_2 = subfolder.split("-")[-1][:-1]


    true_pf_dict = pickle.load(open(actual_pf_p, 'r'))

    problem_name = problem_name_1 + "_" + problem_name_2
    all_data[problem_name] = {}
    all_data[problem_name]['evals'] = []
    all_data[problem_name]['gen_dist'] = []
    all_data[problem_name]['igd'] = []
    for repeat in repeats:
        print problem_name
        if "NSGAII" in subfolder:
            file = repeat + "20.txt"
        elif  "SPEA2" in subfolder:
            file = repeat + "20.txt"
        elif "SWAY5" in subfolder:
            file = repeat + "1.txt"

        # Extract Objectives
        predicted_pf = []
        content = open(file, "r").readlines()
        for c in content:
            predicted_pf.append(map(float, ([cc.strip() for cc in c.split(',')[-2:]])))
            assert (len(predicted_pf[-1]) == 2), "Something is wrong"

        correct_key = [key for key in true_pf_dict.keys() if problem_name_1 in key and problem_name_2 in key]
        assert(len(correct_key) == 1), "Somethign is wrong"
        correct_key = correct_key[-1]

        true_pf = true_pf_dict[correct_key]['pf']
        assert(len(true_pf) > 0), "Somethign is wrong"

        all_data[problem_name]['evals'].append(2100)
        all_data[problem_name]['gen_dist'].append(generational_distance(true_pf, predicted_pf, ranges[correct_key]))
        all_data[problem_name]['igd'].append(inverted_generational_distance(true_pf, predicted_pf, ranges[correct_key]))

        print ". ",
    print


pickle.dump(all_data, open("SWAY5_monrp.p", "w"))





