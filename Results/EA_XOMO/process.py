from __future__ import division
import pickle
import os
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import generational_distance, inverted_generational_distance
import pickle

ranges = {}
ranges['./Data/xomo_all-p10000-d27-o4-dataset1.csv'] = [[3.707966726,26666.23383],[4.568049924,106.5319281]]
ranges['./Data/xomo_all-p10000-d27-o4-dataset2.csv'] = [[4.568049924,106.5319281],[6.685393736,418716.0161]]
ranges['./Data/xomo_all-p10000-d27-o4-dataset3.csv'] = [[6.685393736,418716.0161],[0.0,14.74530831]]
ranges['./Data/xomo_flight-p10000-d27-o4-dataset1.csv'] = [[6.047222022,28742.58749],[5.348895805,100.3527152]]
ranges['./Data/xomo_flight-p10000-d27-o4-dataset2.csv'] = [[5.348895805,100.3527152],[11.4472631,540128.325]]
ranges['./Data/xomo_flight-p10000-d27-o4-dataset3.csv'] = [[11.4472631,540128.325],[0.0,13.94101877]]
ranges['./Data/xomo_ground-p10000-d27-o4-dataset1.csv'] = [[5.047456138,25727.32014],[4.199017713,110.4968852]]
ranges['./Data/xomo_ground-p10000-d27-o4-dataset2.csv'] = [[4.199017713,110.4968852],[10.69176728,345890.7844]]
ranges['./Data/xomo_ground-p10000-d27-o4-dataset3.csv'] = [[10.69176728,345890.7844],[0.0,14.4772118]]
ranges['./Data/xomo_osp-p10000-d27-o4-dataset1.csv'] = [[7.334722936,38227.17263],[5.045540178,103.3070284]]
ranges['./Data/xomo_osp-p10000-d27-o4-dataset2.csv'] = [[5.045540178,103.3070284],[11.22363568,605891.2366]]
ranges['./Data/xomo_osp-p10000-d27-o4-dataset3.csv'] = [[11.22363568,605891.2366],[0.0,15.28150134]]
ranges['./Data/xomoo2-p10000-d27-o4-dataset1.csv'] = [[3.402253099,31456.09489],[4.440279507,99.7843957]]
ranges['./Data/xomoo2-p10000-d27-o4-dataset2.csv'] = [[4.440279507,99.7843957],[5.540869257,418688.4863]]
ranges['./Data/xomoo2-p10000-d27-o4-dataset3.csv'] = [[5.540869257,418688.4863],[0.0,15.28150134]]


actual_pf_p = "./ActualPF/consolidated_dict.p"
folder = "./Data/"
subfolders = [folder + f + "/" for f in os.listdir(folder) if ".DS_Store" not in f]

all_data = {}

evals = {}
evals["NSGAII"] = 2100
evals["SPEA2"] = 2100
evals["SWAY5"] = 70



def run(name):
    for subfolder in subfolders:
        repeats = [subfolder + f + "/" for f in os.listdir(subfolder) if ".DS_Store" not in f]
        print subfolder
        if name not in subfolder: continue

        if "NSGAII" in subfolder or "SPEA2" in subfolder:
            # Find appropriate file
            problem_name_1 = "_".join(subfolder.split('/')[-2].split('_')[1:3])
            problem_name_1 = problem_name_1 if problem_name_1 != "xomo_o2" else 'xomoo2'
            problem_name_2 = "_".join(subfolder.split('/')[-2].split('_')[3:-1])
            if problem_name_2 == "1_2":
                problem_name_2 = "dataset1"
            if problem_name_2 == "2_3":
                problem_name_2 = "dataset2"
            if problem_name_2 == "3_4":
                problem_name_2 = "dataset3"

        elif "SWAY5" in subfolder:
            # Find appropriate file
            problem_name_1 = "_".join(subfolder.split('/')[-2].split('_')[1:3])
            problem_name_1 = problem_name_1 if problem_name_1 != "xomo_o2" else 'xomoo2'
            problem_name_2 = "_".join(subfolder.split('/')[-2].split('_')[3:-1])
            if problem_name_2 == "1_2":
                problem_name_2 = "dataset1"
            if problem_name_2 == "2_3":
                problem_name_2 = "dataset2"
            if problem_name_2 == "3_4":
                problem_name_2 = "dataset3"


        true_pf_dict = pickle.load(open(actual_pf_p, 'r'))

        problem_name = problem_name_1 + "_" + problem_name_2
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
            elif "SWAY5" in subfolder:
                file = repeat + "1.txt"

            # Extract Objectives
            predicted_pf = []
            content = open(file, "r").readlines()
            for c in content:
                predicted_pf.append(map(float, ([cc.strip() for cc in c.split(',')[-2:]])))
                assert (len(predicted_pf[-1]) == 2), "Something is wrong"

            correct_key = [key for key in true_pf_dict.keys() if problem_name_1 in key and problem_name_2 in key]
            print ">>", correct_key
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

            print ". ",
        print

        import pdb
        pdb.set_trace()
    pickle.dump(all_data, open(name + "_XOMO.p", "w"))




for name in ["SPEA2", "NSGAII", "SWAY5"]:
    run(name)
