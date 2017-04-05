from __future__ import division
import pandas as pd

files = ['./Data/llvm_input.csv', './Data/noc_CM_log.csv',
             './Data/rs-6d-c3.csv', './Data/sort_256.csv',
             './Data/wc+rs-3d-c4.csv', './Data/wc+sol-3d-c4.csv', './Data/wc+wc-3d-c4.csv',
             './Data/wc-3d-c4.csv', './Data/wc-5d-c5.csv', './Data/wc-6d-c1.csv', './Data/wc-c1-3d-c1.csv',
             './Data/wc-c3-3d-c1.csv']
ranges = {}
for file in files:
    content = open(file).readlines()
    objectives = []
    for i, c in enumerate(content):
        if i == 0: continue
        values = map(float, c.strip().split(','))
        objectives.append(values[-2:])
    obj1 = [x[0] for x in objectives]
    obj2 = [x[1] for x in objectives]

    range1 = max(obj1) - min(obj1)
    range2 = max(obj2) - min(obj2)
    ranges[file] = [[min(obj1), max(obj1)], [min(obj2), max(obj2)]]

for key in ranges:
    print "ranges[\"" + key + "\"] = ", ranges[key]
