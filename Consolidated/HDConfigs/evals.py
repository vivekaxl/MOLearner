
from __future__ import division
import pickle
import os
from sk_table import rdivDemo


def get_gd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))

        epal_001 = pickle.load(open('epal-based-0.01_Config.p'))
        epal_002 = pickle.load(open('epal-based-0.02_Config.p'))
        epal_004 = pickle.load(open('epal-based-0.04_Config.p'))
        epal_008 = pickle.load(open('epal-based-0.08_Config.p'))
        epal_012 = pickle.load(open('epal-based-0.12_Config.p'))
        epal_016 = pickle.load(open('epal-based-0.16_Config.p'))
        epal_020 = pickle.load(open('epal-based-0.2_Config.p'))
        epal_030 = pickle.load(open('epal-based-0.3_Config.p'))

        mmre = pickle.load(open('mmre-based_Config.p'))
        rank = pickle.load(open('rank-based_Config.p'))



        lists = list()
        try:
            lists.append(['AL2'] + al2[problem]['gen_dist'])
        except:
            pass
        # try:
        #     lists.append(['AL'] + al[problem]['gen_dist'])
        # except:
        #     pass

        # flash3 = pickle.load(open('Flash3.p'))
        # lists.append(['Flash3'] + flash3[problem]['gen_dist'])

        # try:
        #     lists.append(['MMRE'] + mmre[problem]['evals'])
        # except:
        #     pass
        # try:
        #     lists.append(['Rank'] + rank[problem]['evals'])
        # except:
        #     pass
        try:
            lists.append(['epal\_0.01'] + epal_001[problem]['gen_dist'])
        except:
            pass
        # try:
        #     lists.append(['epal\_0.02'] + epal_002[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.04'] + epal_004[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.08'] + epal_008[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.12'] + epal_012[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.16'] + epal_016[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.20'] + epal_020[problem]['gen_dist'])
        # except:
        #     pass
        try:
            lists.append(['epal\_0.30'] + epal_030[problem]['gen_dist'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
    return ret_dict


def get_igd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))

        epal_001 = pickle.load(open('epal-based-0.01_Config.p'))
        epal_002 = pickle.load(open('epal-based-0.02_Config.p'))
        epal_004 = pickle.load(open('epal-based-0.04_Config.p'))
        epal_008 = pickle.load(open('epal-based-0.08_Config.p'))
        epal_012 = pickle.load(open('epal-based-0.12_Config.p'))
        epal_016 = pickle.load(open('epal-based-0.16_Config.p'))
        epal_020 = pickle.load(open('epal-based-0.2_Config.p'))
        epal_030 = pickle.load(open('epal-based-0.3_Config.p'))

        mmre = pickle.load(open('mmre-based_Config.p'))
        rank = pickle.load(open('rank-based_Config.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem]['igd'])
        except:
            pass
        # try:
        #     lists.append(['AL'] + al[problem]['igd'])
        # except:
        #     pass
        # flash3 = pickle.load(open('Flash3.p'))
        # lists.append(['Flash3'] + flash3[problem]['igd'])
        # try:
        #     lists.append(['MMRE'] + mmre[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['Rank'] + rank[problem]['igd'])
        # except:
        #     pass
        try:
            lists.append(['epal\_0.01'] + epal_001[problem]['igd'])
        except:
            pass
        # try:
        #     lists.append(['epal\_0.02'] + epal_002[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.04'] + epal_004[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.08'] + epal_008[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.12'] + epal_012[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.16'] + epal_016[problem]['igd'])
        # except:
        #     pass
        # try:
        #     lists.append(['epal\_0.20'] + epal_020[problem]['igd'])
        # except:
        #     pass
        try:
            lists.append(['epal\_0.30'] + epal_030[problem]['igd'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists,globalMinMax=False)
    return ret_dict


def get_eval_rank(problems):
    return_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))

        epal_001 = pickle.load(open('epal-based-0.01_Config.p'))
        epal_002 = pickle.load(open('epal-based-0.02_Config.p'))
        epal_004 = pickle.load(open('epal-based-0.04_Config.p'))
        epal_008 = pickle.load(open('epal-based-0.08_Config.p'))
        epal_012 = pickle.load(open('epal-based-0.12_Config.p'))
        epal_016 = pickle.load(open('epal-based-0.16_Config.p'))
        epal_020 = pickle.load(open('epal-based-0.2_Config.p'))
        epal_030 = pickle.load(open('epal-based-0.3_Config.p'))

        mmre = pickle.load(open('mmre-based_Config.p'))
        rank = pickle.load(open('rank-based_Config.p'))


        lists = list()
        try: lists.append(['AL2'] + al2[problem]['evals'])
        except: pass
        # try: lists.append(['AL'] + al[problem]['evals'])
        # except:
        #     pass
        # flash3 = pickle.load(open('Flash3.p'))
        # lists.append(['Flash3'] + flash3[problem]['evals'])

        # try: lists.append(['MMRE'] + mmre[problem]['evals'])
        # except:
        #     pass
        # try: lists.append(['Rank'] + rank[problem]['evals'])
        # except:
        #     pass
        try:lists.append(['epal\_0.01'] + epal_001[problem]['evals'])
        except: pass
        # try: lists.append(['epal\_0.02'] + epal_002[problem]['evals'])
        # except: pass
        # try: lists.append(['epal\_0.04'] + epal_004[problem]['evals'])
        # except: pass
        # try: lists.append(['epal\_0.08'] + epal_008[problem]['evals'])
        # except: pass
        # try: lists.append(['epal\_0.12'] + epal_012[problem]['evals'])
        # except: pass
        # try: lists.append(['epal\_0.16'] + epal_016[problem]['evals'])
        # except: pass
        # try: lists.append(['epal\_0.20'] + epal_020[problem]['evals'])
        # except: pass
        try: lists.append(['epal\_0.30'] + epal_030[problem]['evals'])
        except: pass

        return_dict[problem] = rdivDemo("SS"+ str(i+1), problem.replace('_', '\_'), lists, globalMinMax=False)

    return return_dict

# dict = {}
# problems = ['llvm_input.p', 'noc_CM_log.p', 'rs-6d-c3.p', 'sort_256.p', 'wc+rs-3d-c4.p', 'wc+sol-3d-c4.p',
#                 'wc+wc-3d-c4.p', 'wc-3d-c4.p', 'wc-5d-c5.p', 'wc-6d-c1.p', 'wc-c1-3d-c1.p', 'wc-c3-3d-c1.p']
# dict['gd'] = get_gd_rank(problems)
# dict['igd'] = get_igd_rank(problems)
# dict['evals'] = get_eval_rank(problems)
#
# assert(len(dict['gd'].keys()) == len(dict['igd'].keys())), "Something is wrong"
# assert(len(dict['gd'].keys()) == len(dict['evals'].keys())), "Something is wrong"
#
# pickle.dump(dict, open('stat_result.p', 'w'))

def r(data): return round(data, 2)

dict = pickle.load(open('stat_result.p'))

columns_dict = {'sort_256': 3, 'wc-c3-3d-c1': 3,
                'noc_CM_log': 4,
                 'wc-6d-c1': 6,  'wc-c1-3d-c1': 3,
                'wc-5d-c5': 5,  'wc+wc-3d-c4': 3,
                 'wc-3d-c4': 3,  'wc+rs-3d-c4': 3, 'rs-6d-c3': 6,
                'llvm_input': 11, 'wc+sol-3d-c4': 3, }

algorithms = ['AL2', 'epal0.01', 'epal0.3',]
problems = [ 'TriMesh_1_2.p', 'x264-DB_2_3.p', 'SaC1_2.p', ]
all_evals = {}
for i, algorithm in enumerate(algorithms):
    temp = []
    for problem in problems:
        print algorithm, problem
        try:
            temp.append(dict['evals'][problem][algorithm][1])

            print temp[-1]
        except:
            temp.append(0)
    all_evals[algorithm] = temp


import matplotlib.pyplot as plt
import numpy as np
N = len(problems)

import pdb
pdb.set_trace()
space = 9
ind = np.arange(space, space * (len(problems) + 1), space)  # the x locations for the groups
width = 1.5  # the width of the bars

fig, ax = plt.subplots()
al2 = all_evals['AL2']
rects1 = ax.bar(ind, al2, width, color='#DD451F',label='Lives=2')

epal1 = all_evals['epal0.01']
rects2 = ax.bar(ind + 1 * width, epal1, width, color='#4B514C',label='Lives=3')

epal3 = all_evals['epal0.30']
rects3 = ax.bar(ind + 2 * width, epal3, width, color='#626B64',label='Lives=4')

plt.show()
# import pdb
# pdb.set_trace(&