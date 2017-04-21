from __future__ import division
import pickle
import os
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import generational_distance, inverted_generational_distance
import pickle

ranges = {}
ranges['./Data/POM3A-p10000-d9-o3-dataset1.csv'] = [[0.0,3062.535883],[0.0,1.0]]
ranges['./Data/POM3A-p10000-d9-o3-dataset2.csv'] = [[0.0,1.0],[0.0,0.75]]
ranges['./Data/POM3B-p10000-d9-o3-dataset1.csv'] = [[778.3536022,35726.28611],[-2.22e-16,0.978315244]]
ranges['./Data/POM3B-p10000-d9-o3-dataset2.csv'] = [[-2.22e-16,0.978315244],[0.0,0.84]]
ranges['./Data/POM3C-p10000-d9-o3-dataset1.csv'] = [[208.1210074,2739.229785],[0.382683551,0.713683473]]
ranges['./Data/POM3C-p10000-d9-o3-dataset2.csv'] = [[0.382683551,0.713683473],[0.0,0.699669967]]
ranges['./Data/POM3D-p10000-d9-o3-dataset1.csv'] = [[0.0,1541.659687],[0.0,1.0]]
ranges['./Data/POM3D-p10000-d9-o3-dataset2.csv'] = [[0.0,1.0],[0.0,0.727272727]]


actual_pf_p = "./ActualPF/consolidated_dict.p"
folder = "./Data/"
subfolders = [folder + f + "/" for f in os.listdir(folder) if ".DS_Store" not in f]

all_data = {}

evals = {}
evals["NSGAII"] = 2100
evals["SPEA2"] = 2100
evals["SWAY5"] = 70

name = "SWAY5"

for subfolder in subfolders:
    repeats = [subfolder + f + "/" for f in os.listdir(subfolder) if ".DS_Store" not in f]
    print subfolder
    if name not in subfolder: continue

    if "NSGAII" in subfolder or "SPEA2" in subfolder:
        # Find appropriate file
        problem_name_1 = subfolder.split('/')[-2].split('_')[1]
        problem_name_2 = "_".join(subfolder.split('/')[-2].split('_')[2:-1])
        if problem_name_2 == "1_2":
            problem_name_2 = "dataset1"
        if problem_name_2 == "2_3":
            problem_name_2 = "dataset2"

    elif "SWAY5" in subfolder:
        # Find appropriate file
        problem_name_1 = subfolder.split('/')[-2].split('_')[1]
        problem_name_2 = "_".join(subfolder.split('/')[-2].split('_')[2:-1])
        if problem_name_2 == "1_2":
            problem_name_2 = "dataset1"
        if problem_name_2 == "2_3":
            problem_name_2 = "dataset2"

    true_pf_dict = pickle.load(open(actual_pf_p, 'r'))

    problem_name = problem_name_1 + "_" + problem_name_2
    all_data[problem_name] = {}
    all_data[problem_name]['evals'] = []
    all_data[problem_name]['gen_dist'] = []
    all_data[problem_name]['igd'] = []
    for repeat in repeats:
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
        # print correct_key
        assert(len(correct_key) == 1), "Somethign is wrong"
        correct_key = correct_key[-1]

        true_pf = true_pf_dict[correct_key]['pf']
        assert(len(true_pf) > 0), "Somethign is wrong"

        all_data[problem_name]['evals'].append(evals[name])
        all_data[problem_name]['gen_dist'].append(generational_distance(true_pf, predicted_pf, ranges[correct_key]))
        all_data[problem_name]['igd'].append(inverted_generational_distance(true_pf, predicted_pf, ranges[correct_key]))

        print ". ", problem_name
    print


pickle.dump(all_data, open(name + "_POM.p", "w"))





