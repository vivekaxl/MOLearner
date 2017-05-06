from __future__ import division
import pickle
import os
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import generational_distance, inverted_generational_distance
import pickle

ranges = {}
ranges["./Data/MONRP_50_4_5_4_110.csv"] =  [[92403.0, 95344.0], [428.0, 696.0], [99370.0, 99627.0]]
ranges["./Data/POM3B.csv"] =  [[0.0, 34227.640271599994], [0.0, 1.0], [0.0, 0.827586206897]]
ranges["./Data/xomo_all.csv"] =  [[5.8900921014900005, 28583.461233399998], [5.70862368202, 98.79220126530001], [14.9038336217, 791879.990629], [0.0, 14.745308310999999]]
ranges["./Data/xomo_flight.csv"] =  [[5.07704875571, 23004.2641148], [5.79962055412, 98.2239438536], [10.6753616341, 428117.623585], [0.0, 13.941018766800001]]
ranges["./Data/POM3A.csv"] =  [[50.41390895399999, 2884.36190927], [-2.22044604925e-16, 0.841889480617], [0.0, 0.7539882451719999]]
ranges["./Data/POM3D.csv"] =  [[0.0, 1459.07484037], [-2.22044604925e-16, 1.0], [0.0, 0.7272727272730001]]
ranges["./Data/POM3C.csv"] =  [[202.22098459400002, 2776.06783571], [0.36918150500299995, 0.7269238731450001], [0.0, 0.699346405229]]
ranges["./Data/xomo_ground.csv"] =  [[4.784674809519999, 27522.1840857], [4.2245581331699995, 102.89673937799999], [19.1702767897, 372508.726334], [0.0, 13.941018766800001]]
ranges["./Data/xomo_osp.csv"] =  [[4.36140164564, 28090.846327799998], [5.13691252687, 114.196144121], [5.541133544419999, 401407.569903], [0.0, 13.1367292225]]
ranges["./Data/MONRP_50_4_5_0_110.csv"] =  [[94994.0, 97219.0], [452.0, 727.0], [99466.0, 99660.0]]
ranges["./Data/xomoo2.csv"] =  [[4.48249903236, 22162.0418187], [5.76103797422, 103.62850582200001], [8.09558500714, 312806.337078], [0.0, 14.745308310999999]]
ranges["./Data/MONRP_50_4_5_0_90.csv"] =  [[95394.0, 96983.0], [400.0, 605.0], [99341.0, 99574.0]]


actual_pf_p = "./ActualPF/consolidated_dict.p"
folder = "./Data/"
subfolders = [folder + f + "/" for f in os.listdir(folder) if ".DS_Store" not in f]

all_data = {}

evals = {}
evals["NSGAII"] = 2100
evals["SPEA2"] = 2100
evals["MOEAD"] = 2100
evals["SWAY5"] = 70

no_objectives = 4

def run(name):
    for subfolder in subfolders:
        repeats = [subfolder + f + "/" for f in os.listdir(subfolder) if ".DS_Store" not in f]
        print subfolder
        if name not in subfolder: continue

        if "NSGAII" in subfolder or "SPEA2" in subfolder or "MOEAD" in subfolder:
            # Find appropriate file
            problem_name = "_".join(subfolder.split('/')[-2].split('_')[1:-1])

        elif "SWAY5" in subfolder:

            # Find appropriate file
            problem_name = "_".join(subfolder.split('/')[-2].split('_')[1:-1])

        true_pf_dict = pickle.load(open(actual_pf_p, 'r'))

        print problem_name
        all_data[problem_name] = {}
        all_data[problem_name]['evals'] = []
        all_data[problem_name]['gen_dist'] = []
        all_data[problem_name]['igd'] = []
        for repeat in repeats:
            if "NSGAII" in subfolder:
                file = repeat + "20.txt"
            elif  "SPEA2" in subfolder:
                file = repeat + "20.txt"
            elif  "MOEAD" in subfolder:
                file = repeat + "20.txt"
            elif "SWAY5" in subfolder:
                file = repeat + "1.txt"

            # Extract Objectives
            predicted_pf = []
            content = open(file, "r").readlines()
            for c in content:
                predicted_pf.append(map(float, ([cc.strip() for cc in c.split(',')[-1 * no_objectives:]])))
                assert (len(predicted_pf[-1]) == no_objectives), "Something is wrong"

            correct_key = [key for key in true_pf_dict.keys() if problem_name in key]
            # print ">>", correct_key
            try:
                assert(len(correct_key) == 1), "Somethign is wrong"
            except:
                import pdb
                pdb.set_trace()
            correct_key = correct_key[-1]

            true_pf = true_pf_dict[correct_key]['pf']
            assert(len(true_pf) > 0), "Somethign is wrong"


            all_data[problem_name]['evals'].append(evals[name])
            all_data[problem_name]['gen_dist'].append(generational_distance(true_pf, predicted_pf, ranges[correct_key]))
            all_data[problem_name]['igd'].append(inverted_generational_distance(true_pf, predicted_pf, ranges[correct_key]))

            print ". ", problem_name
        print

    pickle.dump(all_data, open(name + "_XOMO.p", "w"))




for name in ["NSGAII", "SWAY5", "SPEA2", "MOEAD"]:
    run(name)
