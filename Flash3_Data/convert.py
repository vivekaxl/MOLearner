import pickle
import os

files = [
    # 'llvm_input',
    # 'noc_CM_log',
    # 'sort_256',
    # 'wc+rs-3d-c4',
    # 'wc+sol-3d-c4',
    # 'wc+wc-3d-c4',
    # 'wc-3d-c4',
    # 'wc-5d-c5',
    # 'wc-6d-c1',
    # 'wc-c1-3d-c1',
    # 'wc-c3-3d-c1',
    # 'rs-6d-c3',
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

all_data = {}
for file in files:
    print file
    if file != "wc-3d-c4":
        all_pickle_files = ["./PickleLocker/" + f for f in os.listdir("./PickleLocker/") if file in f]
    else:
        all_pickle_files = ["./PickleLocker/" + f for f in os.listdir("./PickleLocker/") if file in f and "+" not in f]

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

pickle.dump(all_data, open("Flash3.p", "w"))
