from __future__ import division
import pandas as pd

files = [
        './Data/POM3A.csv',
        './Data/POM3B.csv',
        './Data/POM3C.csv',
        './Data/POM3D.csv', './Data/xomo_all.csv',
        './Data/xomo_flight.csv',
        './Data/xomo_ground.csv',
        './Data/xomo_osp.csv',
        './Data/xomoo2.csv','./Data/xomo_all.csv',
        './Data/MONRP_50_4_5_0_110.csv',
        './Data/MONRP_50_4_5_0_90.csv',
        './Data/MONRP_50_4_5_4_110.csv',
        './Data/MONRP_50_4_5_4_90.csv',

    ]
ranges = {}
for file in files:
    content = open(file).readlines()
    objectives = []
    content = pd.read_csv(file)
    columns = [c for c in content.columns if '<$' in c]
    objectives = content[columns].values.tolist()
    temp_ranges = []
    for i in xrange(len(columns)):
        temp_obj = [obj[i] for obj in objectives]
        temp_ranges.append([min(temp_obj), max(temp_obj)])
    ranges[file] = temp_ranges

for key in ranges:
    print "ranges[\"" + key + "\"] = ", ranges[key]
