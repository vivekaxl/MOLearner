import pickle
import numpy as np

content = pickle.load(open("epal.p"))
files = content.keys()

const_files = [
    "./Data/wc-3d-c4.csv",
    "./Data/llvm_input.csv",
    "./Data/noc_CM_log.csv",
    "./Data/rs-6d-c3.csv",
    "./Data/sort_256.csv",
    "./Data/wc+rs-3d-c4.csv",
    "./Data/wc+sol-3d-c4.csv",
    "./Data/wc+wc-3d-c4.csv",
    "./Data/wc-5d-c5.csv",
    "./Data/wc-6d-c1.csv",
    "./Data/wc-c1-3d-c1.csv",
    "./Data/wc-c3-3d-c1.csv",
        ]

assert(len(files) == len(const_files)), "Something is wrong"

keys = ['evals', 'igd', 'gen_dist']
key = 'igd'

epsilon_values = [0.01, 0.02, 0.04, 0.08, 0.12, 0.16, 0.2, 0.3]

# print "Name", " ".join(map(str, epsilon_values))
for file in const_files:
    # print file.split('/')[-1],
    for epsilon_value in epsilon_values:
        print round(np.median(content[file][epsilon_value][key]), 3),
    print
