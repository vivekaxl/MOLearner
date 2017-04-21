from __future__ import division
import pickle
import os


def run(name):
    files = ["./Data/" + f for f in os.listdir("./Data/") if ".p" in f]
    all_data = {}
    for file in files:
        if name + '-based' not in file: continue
        content = pickle.load(open(file))
        filename = file.split("/")[-1]
        method_name = filename.split('_')[0]

        problem_name_1 = "_".join(filename.replace('-', '_').split("_")[2:8])
        problem_name_2 = filename.replace('-', '_').split("_")[-1].split(".")[0]
        problem_name = problem_name_1 + "_" + problem_name_2

        all_data[problem_name] = {}
        all_data[problem_name]['evals'] = content[content.keys()[-1]]['evals']
        all_data[problem_name]['gen_dist'] = content[content.keys()[-1]]['gen_dist']
        all_data[problem_name]['igd'] = content[content.keys()[-1]]['igd']

        print ". ", problem_name
    print

    pickle.dump(all_data, open(name + "_monrp.p", "w"))


names = ['al', 'al2', 'rank', 'mmre']
for name in names:
    run(name)