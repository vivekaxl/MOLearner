
from __future__ import division
import pickle
import os
from sk_rank import rdivDemo


def get_gd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_monrp.p'))
        al = pickle.load(open('al_monrp.p'))

        nsgaii = pickle.load(open('nsgaii_monrp.p'))
        spea2 = pickle.load(open('spea2_monrp.p'))
        sway5 = pickle.load(open('SWAY5_monrp.p'))

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
            lists.append(['NSGAII'] + nsgaii[problem]['evals'])
        except:
            pass
        try:
            lists.append(['SPEA2'] + spea2[problem]['evals'])
        except:
            pass
        try:
            lists.append(['SWAY'] + sway5[problem]['evals'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
    return ret_dict


def get_igd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_monrp.p'))
        al = pickle.load(open('al_monrp.p'))

        nsgaii = pickle.load(open('nsgaii_monrp.p'))
        spea2 = pickle.load(open('spea2_monrp.p'))
        sway5 = pickle.load(open('SWAY5_monrp.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem]['igd'])
        except:
            pass
        try:
            lists.append(['AL'] + al[problem]['igd'])
        except:
            pass

        try:
            lists.append(['NSGAII'] + nsgaii[problem]['igd'])
        except:
            pass
        try:
            lists.append(['SPEA2'] + spea2[problem]['igd'])
        except:
            pass
        try:
            lists.append(['SWAY'] + sway5[problem]['igd'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists,globalMinMax=False)
    return ret_dict


def get_eval_rank(problems):
    return_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_monrp.p'))
        al = pickle.load(open('al_monrp.p'))

        nsgaii = pickle.load(open('nsgaii_monrp.p'))
        spea2 = pickle.load(open('spea2_monrp.p'))
        sway = pickle.load(open('SWAY5_monrp.p'))

        lists = list()
        try: lists.append(['AL2'] + al2[problem]['evals'])
        except: pass
        try: lists.append(['AL'] + al[problem]['evals'])
        except:
            pass
        try:lists.append(['NSGAII'] + nsgaii[problem]['evals'])
        except: pass
        try: lists.append(['SPEA2'] + spea2[problem]['evals'])
        except: pass
        try: lists.append(['SWAY'] + sway[problem]['evals'])
        except: pass

        return_dict[problem] = rdivDemo("SS"+ str(i+1), problem.replace('_', '\_'), lists, globalMinMax=False)

    return return_dict

# dict = {}
# problems = ['MONRP_50_4_5_0_110_dataset1', 'MONRP_50_4_5_0_90_dataset2', 'MONRP_50_4_5_0_90_dataset1',
#             'MONRP_50_4_5_0_110_dataset2', 'MONRP_50_4_5_4_110_dataset1', 'MONRP_50_4_5_4_110_dataset2',
#             'MONRP_50_4_5_4_90_dataset1', 'MONRP_50_4_5_4_90_dataset2']
# dict['gd'] = get_gd_rank(problems)
# dict['igd'] = get_igd_rank(problems)
# dict['evals'] = get_eval_rank(problems)
#
# assert(len(dict['gd'].keys()) == len(dict['igd'].keys())), "Something is wrong"
# assert(len(dict['gd'].keys()) == len(dict['evals'].keys())), "Something is wrong"
#
# pickle.dump(dict, open('stat_result.p', 'w'))

dict = pickle.load(open('stat_result.p'))
algorithms = ['AL', 'AL2', 'NSGAII', 'SPEA2', 'SWAY']
problems = ['MONRP_50_4_5_0_110_dataset1', 'MONRP_50_4_5_0_110_dataset2', 'MONRP_50_4_5_0_90_dataset1', 'MONRP_50_4_5_0_90_dataset2', 'MONRP_50_4_5_4_110_dataset1', 'MONRP_50_4_5_4_110_dataset2', 'MONRP_50_4_5_4_90_dataset1', 'MONRP_50_4_5_4_90_dataset2']
header = "\multirow{3}{*}{Name} & \multicolumn{6}{l|}{Greedy} & \multicolumn{9}{l|}{EA}                                                                     \\ \cline{2-11}\n"
header += "& \multicolumn{3}{l|}{AL1}          & \multicolumn{3}{l|}{AL2} & \multicolumn{3}{l|}{NSGAII} & \multicolumn{3}{l|}{SPEA2} & \multicolumn{3}{l|}{SWAY} \\\ \hline \n"
header += " \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals}gi"
print header
for problem in problems:
    print problem.replace('_', '\_'), '&',
    for i, algorithm in enumerate(algorithms):
        if dict['gd'][problem][algorithm] == 1: print '\cellcolor[HTML]{67FD9A} &',
        else: print '\cellcolor[HTML]{FFFE65} &',

        if dict['igd'][problem][algorithm] == 1: print '\cellcolor[HTML]{67FD9A} &',
        else: print '\cellcolor[HTML]{FFFE65} &',
        if dict['evals'][problem][algorithm] == 1: print '\cellcolor[HTML]{67FD9A}',
        else: print "\cellcolor[HTML]{FFFE65}",
        if i + 1 != len(algorithms): print '&',
    print '\\\ \hline'

# import pdb
# pdb.set_trace(&