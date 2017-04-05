from __future__ import division
import os
import sys
import numpy as np
import pandas as pd
from utility import container

def process(folder):
    """To extract the number of point in the predicted frontier and number of evaluations"""
    subfolders = [folder + subfolder + "/" for subfolder in os.listdir(folder) if os.path.isdir(folder + subfolder)]
    eval_filename = "prediction_error.csv"
    all_data = {}
    for subfolder in subfolders:
        data_dict = {}
        files = [subfolder + f for f in os.listdir(subfolder) if eval_filename not in f and 'stop' not in f and ".csv" in f]
        for file in files:
            # Extract the filename in the file path
            filename = file.split('/')[-1]
            # remove predicted_pareto from the filename
            filename = filename.replace('predicted_pareto_', '')
            # remove .csv from the filename
            filename = filename.replace('.csv', '')
            # extract the repeat number
            repeat_no = filename.split('_')[0]
            epsilon_value = filename.split('_')[1]
            content = open(file).readlines()
            number_of_lines = sum([1 for _ in content])
            if epsilon_value not in data_dict.keys():
                data_dict[epsilon_value] = container(subfolder, epsilon_value)
            data_dict[epsilon_value].append_pfs(number_of_lines)

        eval_filepath = subfolder + eval_filename
        evals_df = pd.read_csv(eval_filepath, header=None)
        # This is the format of the eval_filname: rep_iter, epsilon,num_evaluations,avg_epsilon_perc_obj1,state.
        # total_time,pop_sampled.num_entries
        repeats = evals_df[0].unique().tolist()
        epsilons = evals_df[1].unique().tolist()
        for epsilon in epsilons:
            temp_df = evals_df[evals_df[1] == epsilon]
            data_dict[str(epsilon)].set_evals(temp_df[2].tolist())

        all_data[subfolder] = data_dict

    import pickle
    pickle.dump(all_data, open('results.p', 'w'))

    csv_data = [['filename', 'epsilon', 'mean-size-of-PF', 'no-evals']]
    # Iterating through all the files
    for key in all_data.keys():
        # Iterating through all epsilons
        for sec_key in all_data[key]:
            csv_data.append([key.replace('./Data/results_', '')[:-1], sec_key, np.mean(all_data[key][sec_key].pfs), np.mean(all_data[key][sec_key].evals)])

    import csv
    with open("results.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


def validity_check(folder):
    # quick check
    subfolders = [folder + subfolder + "/" for subfolder in os.listdir(folder) if os.path.isdir(folder + subfolder)]
    eval_filename = "prediction_error.csv"
    for subfolder in subfolders:
        eval_filepath = subfolder + eval_filename
        content = open(eval_filepath).readlines()
        number_of_lines = sum([1 for _ in content])
        # All the files except for results_sol-6d-c2 should have 320 lines
        if number_of_lines != 320:
            print eval_filepath
        # All the lines should have 6 comma separated values
        for i, c in enumerate(content):
            no_fields = len(content[i].strip().split(','))
            if no_fields != 6:
                print "no_fields: ", eval_filepath, " | ", content[i]


if __name__ == "__main__":
    folder = "./Data/"
    process(folder)

