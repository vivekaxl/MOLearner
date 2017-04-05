from __future__ import division
import os
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import generational_distance, ranges
from utility import container

# mapping between pareto data and raw data
raw_mapping = {}
raw_mapping["results_llvm/"] = "llvm_input.csv"
raw_mapping["results_noc_cm/"] = "noc_CM_log.csv"
raw_mapping["results_sort_256/"] = "sort_256.csv"
raw_mapping["results_rs-6d-c3/"] = "rs-6d-c3.csv"
raw_mapping["results_sol-6d-c2/"] = "sol-6d-c2.csv"
raw_mapping["results_wc+wc-3d-c4/"] = "wc+wc-3d-c4.csv"
raw_mapping["results_wc-3d-c4/"] = "wc-3d-c4.csv"
raw_mapping["results_wc-5d-c5/"] = "wc-5d-c5.csv"
raw_mapping["results_wc-6d-c1/"] = "wc-6d-c1.csv"
raw_mapping["results_wc-c1-3d-c1/"] = "wc-c1-3d-c1.csv"
raw_mapping["results_wc-c3-3d-c1/"] = "wc-c3-3d-c1.csv"
raw_mapping["results_wc+sol-3d-c4/"] = "wc+sol-3d-c4.csv"
raw_mapping["results_wc+rs-3d-c4/"] = "wc+rs-3d-c4.csv"

def process(epsilon_value, predicted_sub_folder, actual_pareto_file, range):
    import pickle
    data_dict = pickle.load(open('results.p', 'r'))
    key = [k for k in data_dict.keys() if predicted_sub_folder.split('/')[-2] in k]
    assert(len(key) == 1), "Something is wrong"
    key = key[-1]
    true_pf = [map(float, line.strip().split(',')) for line in open(actual_pareto_file).readlines()]
    files = [predicted_sub_folder + f for f in os.listdir(predicted_sub_folder)]
    filtered_files = [f for f in files if str(epsilon_value) in f]
    data = {}
    data['evals'] = data_dict[key][str(epsilon_value)].evals
    data['gen_dist'] = []
    for f_file in filtered_files:
        predicted_pf = [map(float, line.strip().split(',')) for line in open(f_file).readlines()]
        data['gen_dist'].append(generational_distance(true_pf, predicted_pf, range))
    return data



if __name__ == "__main__":
    all_data = {}
    actual_folder = "./Actual_Pareto_Data/"
    predicted_folder = "./Predicted_Pareto_Data/"
    predicted_sub_folders = [predicted_folder + f + "/" for f in os.listdir(predicted_folder) if "DS_Store" not in f and "sol-6d-c2" not in f]
    epsilon_values = [0.01, 0.2, 0.02, 0.3, 0.04, 0.08, 0.12, 0.16]
    for predicted_sub_folder in predicted_sub_folders:
        key_all_data = "./Data/" + raw_mapping[predicted_sub_folder.split('/')[-2] + "/"]
        all_data[key_all_data] = {}
        print predicted_sub_folder
        for epsilon_value in epsilon_values:
            print ". ",
            sys.stdout.flush()
            all_data[key_all_data][epsilon_value] = process(epsilon_value, predicted_sub_folder, actual_folder+raw_mapping[predicted_sub_folder.split('/')[-2] + '/'], ranges[key_all_data])
        print
    import pickle
    pickle.dump(all_data, open('epal.p', 'w'))
