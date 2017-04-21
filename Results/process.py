import pickle
import numpy as np
import sys
import os
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import container
import matplotlib.pyplot as plt
from matplotlib import rc


names = [
"xomo_osp-p10000-d27-o4-dataset3.p",
"xomoo2-p10000-d27-o4-dataset2.p",
"MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.p",
"wc+sol-3d-c4.p",
"xomo_ground-p10000-d27-o4-dataset2.p",
"POM3A-p10000-d9-o3-dataset2.p",
"xomo_all-p10000-d27-o4-dataset3.p",
"xomo_ground-p10000-d27-o4-dataset3.p",
"x264-DB_2_3.p",
"POM3D-p10000-d9-o3-dataset1.p",
"xomo_ground-p10000-d27-o4-dataset1.p",
"MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.p",
"POM3B-p10000-d9-o3-dataset2.p",
"x264-DB_1_2.p",
"noc_CM_log.p",
"llvm_input.p",
"MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.p",
"xomo_flight-p10000-d27-o4-dataset3.p",
"SaC_3_4.p",
"POM3C-p10000-d9-o3-dataset1.p",
"POM3B-p10000-d9-o3-dataset1.p",
"TriMesh_2_3.p",
"xomo_flight-p10000-d27-o4-dataset2.p",
"xomo_flight-p10000-d27-o4-dataset1.p",
"xomo_osp-p10000-d27-o4-dataset1.p",
"MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.p",
"x264-DB_3_4.p",
"MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.p",
"wc+rs-3d-c4.p",
"wc+wc-3d-c4.p",
"SaC1_2.p",
"SaC_9_10.p",
"wc-6d-c1.p",
"wc-5d-c5.p",
"x264-DB_5_6.p",
"SaC_11_12.p",
"SaC_5_6.p",
"wc-c1-3d-c1.p",
"POM3C-p10000-d9-o3-dataset2.p",
"MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.p",
"POM3D-p10000-d9-o3-dataset2.p",
"xomo_all-p10000-d27-o4-dataset2.p",
"SaC_7_8.p",
"xomo_all-p10000-d27-o4-dataset1.p",
"xomo_osp-p10000-d27-o4-dataset2.p",
"POM3A-p10000-d9-o3-dataset1.p",
"MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.p",
"rs-6d-c3.p",
"MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.p",
"x264-DB_4_5.p",
"wc-c3-3d-c1.p",
"TriMesh_1_2.p",
"xomoo2-p10000-d27-o4-dataset1.p",
"xomoo2-p10000-d27-o4-dataset3.p",
"sort_256.p",
"_wc-3d-c4.p",
]

results = {}

names_dict = {
    'al-based': "al1",
    'al2-based': "al2",
    'mmre-based': "mmre",
    'rank-based': "rank"
}

for name in names:
    # print name
    # find all the files corresponding to the name
    files = [f for f in os.listdir(".") if ".py" not in f and name in f]
    # print files
    if len(files) != 4:
        print name, files
        continue
    else:
        results[name] = {}
        results[name]['mmre'] = {}
        results[name]['rank'] = {}
        results[name]['al1'] = {}
        results[name]['al2'] = {}
        for key in results[name]:
            for metric in ["evals", "igd", "gen_dist"]:
                results[name][key][metric] = []
        for file in files:
            print file
            for key in names_dict:
                if key in file:
                    print key
                    content = pickle.load(open(file))
                    assert(len(content.keys()) == 1), "Somethign is wrong"
                    c_key = content.keys()[-1]
                    results[name][names_dict[key]]['evals'] = content[c_key]['evals']
                    results[name][names_dict[key]]['igd'] = content[c_key]['igd']
                    results[name][names_dict[key]]['gen_dist'] = content[c_key]['gen_dist']

# consolidated pickle file
pickle.dump(results, open('consolidated_result.p', 'w'))



