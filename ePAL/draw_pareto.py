from __future__ import division
import os
from non_dominated_sort import non_dominated_sort
import sys
import numpy as np
import csv


raw_data_folder = "../Data/"
pareto_data_folder = "./Data/"

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

# Objectives = {}
lessismore = {}
lessismore["results_llvm/"] = [False, False]
lessismore["results_noc_cm/"] = [False, False]
lessismore["results_sort_256/"] = [False, False]
lessismore["results_rs-6d-c3/"] = [False, True]
lessismore["results_sol-6d-c2/"] = [False, True]
lessismore["results_wc+wc-3d-c4/"] = [False, True]
lessismore["results_wc-3d-c4/"] = [False, True]
lessismore["results_wc-5d-c5/"] = [False, True]
lessismore["results_wc-6d-c1/"] = [False, True]
lessismore["results_wc-c1-3d-c1/"] = [False, True]
lessismore["results_wc-c3-3d-c1/"] = [False, True]
lessismore["results_wc+sol-3d-c4/"] = [False, True]
lessismore["results_wc+rs-3d-c4/"] = [False, True]


# assign objective values to pareto data
result_folders = ['results_sort_256/', 'results_wc+rs-3d-c4/', 'results_wc+sol-3d-c4/', 'results_wc+wc-3d-c4/', 'results_wc-3d-c4/', 'results_wc-5d-c5/', 'results_wc-6d-c1/', 'results_wc-c1-3d-c1/', 'results_wc-c3-3d-c1/', 'results_sol-6d-c2/',]

for result_folder in result_folders:
    print "--- " * 10
    print result_folder
    # generate a dict to assign objective values
    objective_dict = {}
    raw_filename = raw_data_folder + raw_mapping[result_folder]
    content = open(raw_filename).readlines()
    duplicate_count = 0
    for i, line in enumerate(content):
        if i == 0: continue
        line_values = map(float, [v for v in line.strip().split(',')])
        independent_values = map(int, line_values[:-2])
        dependent_values = line_values[-2:]
        assert(len(independent_values) + len(dependent_values) == len(line_values)), "Something is wrong"
        independent_key = ",".join(map(str, independent_values))
        if independent_key in objective_dict.keys(): duplicate_count += 1
        objective_dict[independent_key] = dependent_values

    actual_dependent_values = [objective_dict[key] for key in objective_dict.keys()]
    actual_pf_indexes = non_dominated_sort(actual_dependent_values, lessismore[result_folder])
    actual_pf = sorted([actual_dependent_values[index] for index in actual_pf_indexes], key=lambda x:x[1], reverse=True)
    # Store Actual Pareto Data
    pf_store_filename = "./Actual_Pareto_Data/" + raw_mapping[result_folder]
    with open(pf_store_filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(actual_pf)

    # find the objective scores of the pareto front extracted by epal
    pareto_files = [pareto_data_folder + result_folder + f for f in os.listdir(pareto_data_folder + result_folder) if "prediction_error" not in f and 'stop' not in f and ".csv" in f]
    for pareto_file in pareto_files:
        print ". ",pareto_file
        sys.stdout.flush()
        pareto_content = open(pareto_file).readlines()
        assert(len(content) >= len(pareto_content)), "Something is wrong"
        predicted_pareto_front = []
        for pc in pareto_content:
            pc_value = map(int, map(float, pc.strip().split(';')))
            pareto_key = ",".join(map(str, pc_value))
            predicted_pareto_front.append(objective_dict[pareto_key])
        assert(len(predicted_pareto_front) == len(pareto_content)), "Something is wrong"

        nd_pf_indexes = non_dominated_sort(predicted_pareto_front, lessismore[result_folder])
        nd_pf = sorted([predicted_pareto_front[index] for index in nd_pf_indexes], key=lambda x:x[1], reverse=True)
        import matplotlib.pyplot as plt
        plt.scatter([np.log(d[0]) for d in actual_dependent_values], [np.log(d[1]) for d in actual_dependent_values], color='r')
        l1, = plt.plot([np.log(p[0]) for p in nd_pf], [np.log(p[1]) for p in nd_pf], color='black', marker='x', label="Predicted-PF")
        l2, = plt.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='green', marker='o', label="Actual-PF")
        plt.xlabel('log(f1)')
        plt.ylabel('log(f2)')
        plt.legend(loc=2)
        figure_name = "./Figures/" +  "/".join(pareto_file.split('/')[2:])[:-3] + "jpg"
        intermediate_folders = "/".join(figure_name.split('/')[:-1]) + "/"
        try:
            os.makedirs(intermediate_folders)
        except:
            pass
        plt.savefig(figure_name)
        plt.cla()

        # Store Predicted Pareto Data
        pf_store_filename = "./Predicted_Pareto_Data/" +  "/".join(pareto_file.split('/')[2:])
        intermediate_folders = "/".join(pf_store_filename.split('/')[:-1]) + "/"
        try:
            os.makedirs(intermediate_folders)
        except:
            pass
        with open(pf_store_filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(nd_pf)


    print





# import matplotlib.pyplot as plt
# plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r')
# plt.plot([p[0] for p in pf], [p[1] for p in pf], color='black', marker='x')
# plt.show()