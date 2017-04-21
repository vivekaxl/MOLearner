from __future__ import division
import pickle
import os

pickle_files = [f for f in os.listdir(".") if ".py" not in f]

prob = {}

for pickle_file in pickle_files:
    print pickle_file
    content = pickle.load(open(pickle_file))
    problems = content.keys()
    for problem in problems:
        if problem not in prob.keys():
            print pickle_file, problem
            prob[problem] = 1
        else:
            prob[problem] += 1


import pdb
pdb.set_trace()