import pickle
import os

files = [
    'MONRP_50_4_5_0_110',
    'MONRP_50_4_5_0_90',
    'MONRP_50_4_5_4_110',
    'MONRP_50_4_5_4_90',
    'POM3A',
    'POM3B',
    'POM3C',
    'POM3D',
    'xomo_all',
    'xomo_flight',
    'xomo_ground',
    'xomo_osp',
    'xomoo2'
]

# pickle_files = [ f for f in os.listdir('.') if ".p" in f and ".py" not in f]

all_data = {}
for file in files:
    print file
    all_pickle_files = [ f for f in os.listdir('.') if ".p" in f and ".py" not in f and file in f]

    print len(all_pickle_files)
    assert(len(all_pickle_files) == 20), "Something is wrong"
    all_data[file + ".p"] = {}
    all_data[file + ".p"]['gen_dist'] = []
    all_data[file + ".p"]['igd'] = []
    all_data[file + ".p"]['evals'] = []

    for p_files in all_pickle_files:
        temp_content = pickle.load(open(p_files))
        all_data[file + ".p"]['gen_dist'].append(temp_content["./Data/" + file + ".csv"]["gen_dist"][-1])
        all_data[file + ".p"]['igd'].append(temp_content["./Data/" + file + ".csv"]["igd"][-1])
        all_data[file + ".p"]['evals'].append(temp_content["./Data/" + file + ".csv"]["evals"][-1])

    assert(len(all_data[file + ".p"]['gen_dist']) == 20), "Something is wrong"
    assert(len(all_data[file + ".p"]['igd']) == 20), "Something is wrong"
    assert(len(all_data[file + ".p"]['evals']) == 20), "Something is wrong"

pickle.dump(all_data, open("al4.p", "w"))