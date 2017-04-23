
from __future__ import division
import pickle
import os
from sk_rank import rdivDemo


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
            lists.append(['AL2'] + al2[problem]['evals'])
        except:
            pass
        try:
            lists.append(['AL'] + al[problem]['evals'])
        except:
            pass
        # try:
        #     lists.append(['MMRE'] + mmre[problem]['evals'])
        # except:
        #     pass
        # try:
        #     lists.append(['Rank'] + rank[problem]['evals'])
        # except:
        #     pass
        try:
            lists.append(['epal\_0.01'] + epal_001[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.02'] + epal_002[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.04'] + epal_004[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.08'] + epal_008[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.12'] + epal_012[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.16'] + epal_016[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.20'] + epal_020[problem]['evals'])
        except:
            pass
        try:
            lists.append(['epal\_0.30'] + epal_030[problem]['evals'])
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
        try:
            lists.append(['AL'] + al[problem]['igd'])
        except:
            pass
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
        try:
            lists.append(['epal\_0.02'] + epal_002[problem]['igd'])
        except:
            pass
        try:
            lists.append(['epal\_0.04'] + epal_004[problem]['igd'])
        except:
            pass
        try:
            lists.append(['epal\_0.08'] + epal_008[problem]['igd'])
        except:
            pass
        try:
            lists.append(['epal\_0.12'] + epal_012[problem]['igd'])
        except:
            pass
        try:
            lists.append(['epal\_0.16'] + epal_016[problem]['igd'])
        except:
            pass
        try:
            lists.append(['epal\_0.20'] + epal_020[problem]['igd'])
        except:
            pass
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
        try: lists.append(['AL'] + al[problem]['evals'])
        except:
            pass
        # try: lists.append(['MMRE'] + mmre[problem]['evals'])
        # except:
        #     pass
        # try: lists.append(['Rank'] + rank[problem]['evals'])
        # except:
        #     pass
        try:lists.append(['epal\_0.01'] + epal_001[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.02'] + epal_002[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.04'] + epal_004[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.08'] + epal_008[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.12'] + epal_012[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.16'] + epal_016[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.20'] + epal_020[problem]['evals'])
        except: pass
        try: lists.append(['epal\_0.30'] + epal_030[problem]['evals'])
        except: pass

        return_dict[problem] = rdivDemo("SS"+ str(i+1), problem.replace('_', '\_'), lists, globalMinMax=False)

    return return_dict
#
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

dict = pickle.load(open('stat_result.p'))
algorithms = ['AL', 'AL2', 'epal0.01', 'epal0.02', 'epal0.04', 'epal0.08', 'epal0.12', 'epal0.16', 'epal0.20', 'epal0.30']
problems = ['llvm_input.p', 'noc_CM_log.p', 'rs-6d-c3.p', 'sort_256.p', 'wc+rs-3d-c4.p', 'wc+sol-3d-c4.p', 'wc+wc-3d-c4.p', 'wc-3d-c4.p', 'wc-5d-c5.p', 'wc-6d-c1.p', 'wc-c1-3d-c1.p', 'wc-c3-3d-c1.p']
header = "\multirow{3}{*}{Name} & \multicolumn{6}{l|}{Greedy} & \multicolumn{24}{l|}{ePAL}                                                                     \\ \cline{2-11}\n"
header += "& \multicolumn{3}{l|}{AL1}          & \multicolumn{3}{l|}{AL2} & \multicolumn{3}{l|}{ePal-0.01} & \multicolumn{3}{l|}{ePal-0.02} & \multicolumn{3}{l|}{ePal-0.04} & \multicolumn{3}{l|}{ePal-0.08} & \multicolumn{3}{l|}{ePal-0.12} & \multicolumn{3}{l|}{ePal-0.16} & \multicolumn{3}{l|}{ePal-0.20} & \multicolumn{3}{l|}{ePal-0.30} \\\ \hline \n"
header += " \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} &"
print header
for problem in problems:
    print problem.replace('_', '\_'), '&',
    for i, algorithm in enumerate(algorithms):
        if dict['gd'][problem][algorithm] == 1: print '\cellcolor[HTML]{34FF34} &',
        else: print '\cellcolor[HTML]{FE0000} &',

        if dict['igd'][problem][algorithm] == 1: print '\cellcolor[HTML]{34FF34} &',
        else: print '\cellcolor[HTML]{FE0000} &',
        if dict['evals'][problem][algorithm] == 1: print '\cellcolor[HTML]{34FF34}',
        else: print "\cellcolor[HTML]{FE0000}",
        if i + 1 != len(algorithms): print '&',
    print '\\\ \hline'

# import pdb
# pdb.set_trace(&