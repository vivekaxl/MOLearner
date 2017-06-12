
from __future__ import division
import pickle
import os
from sk_table import rdivDemo


def get_gd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al5 = pickle.load(open('al5.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway5 = pickle.load(open('SWAY5_POM.p'))
        moead = pickle.load(open('MOEAD_POM.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem+".p"]['gen_dist'])
        except:
            import pdb
            pdb.set_trace()
            pass
        try:
            lists.append(['AL5'] + al5[problem + ".p"]['gen_dist'])
        except:
            import pdb
            pdb.set_trace()
            pass
        try:
            lists.append(['NSGAII'] + nsgaii[problem]['gen_dist'])
        except:
            pass
        try:
            lists.append(['SPEA2'] + spea2[problem]['gen_dist'])
        except:
            pass
        try:
            lists.append(['SWAY'] + sway5[problem]['gen_dist'])
        except:
            pass
        try:
            lists.append(['MOEAD'] + moead[problem]['gen_dist'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
    return ret_dict


def get_igd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al5 = pickle.load(open('al5.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway5 = pickle.load(open('SWAY5_POM.p'))
        moead = pickle.load(open('MOEAD_POM.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem+".p"]['igd'])
        except:
            pass

        lists.append(['AL5'] + al5[problem+".p"]['igd'])

        # flash3 = pickle.load(open('Flash4.p'))
        # lists.append(['Flash4'] + flash3[problem + ".p"]['igd'])
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
        try:
            lists.append(['MOEAD'] + moead[problem]['igd'])
        except:
            pass

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists,globalMinMax=False)
    return ret_dict


def get_eval_rank(problems):
    return_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al5 = pickle.load(open('al5.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway = pickle.load(open('SWAY5_POM.p'))
        moead = pickle.load(open('MOEAD_POM.p'))

        lists = list()
        try: lists.append(['AL2'] + al2[problem+".p"]['evals'])
        except: pass

        try: lists.append(['AL5'] + al5[problem+".p"]['evals'])
        except:
            pass
        try:lists.append(['NSGAII'] + nsgaii[problem]['evals'])
        except: pass
        try: lists.append(['SPEA2'] + spea2[problem]['evals'])
        except: pass
        try: lists.append(['SWAY'] + sway[problem]['evals'])
        except: pass
        try: lists.append(['MOEAD'] + moead[problem]['evals'])
        except: pass

        return_dict[problem] = rdivDemo("SS"+ str(i+1), problem.replace('_', '\_'), lists, globalMinMax=False)

    return return_dict

dict = {}
problems = ['POM3A', 'POM3B', 'POM3C', 'POM3D']

dict['gd'] = get_gd_rank(problems)
dict['igd'] = get_igd_rank(problems)
dict['evals'] = get_eval_rank(problems)

assert(len(dict['gd'].keys()) == len(dict['igd'].keys())), "Something is wrong"
assert(len(dict['gd'].keys()) == len(dict['evals'].keys())), "Something is wrong"

pickle.dump(dict, open('stat_result.p', 'w'))
def r(data): return round(data, 2)
dict = pickle.load(open('stat_result.p'))
algorithms = [ 'AL2', 'AL5', 'NSGAII', 'SPEA2', 'MOEAD', 'SWAY']
problems = ['POM3A', 'POM3B', 'POM3C', 'POM3D']
header = "\multirow{3}{*}{\\textbf{Model}} & \multirow{3}{*}{\\textbf{\\rot{\# Decisions}}} & \multicolumn{3}{c|}{\multirow{2}{*}{\\textbf{FLASH}}} & \multicolumn{9}{l|}{\\textbf{EA}}                                                                     \\\ \cline{6-14}\n"
header += "& & \multicolumn{3}{l|}{\\textbf{}} & \multicolumn{3}{l|}{\\textbf{NSGAII}} & \multicolumn{3}{l|}{\\textbf{SPEA2}} & \multicolumn{3}{l|}{\\textbf{MOEAD}} & \multicolumn{3}{l|}{\\textbf{SWAY}} \\\ \cline{3-14}\n"
header += "& & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} \\\ \hline"
print header
for problem in problems:
    print problem.replace('_', '\_'), '& 9 &',
    for i, algorithm in enumerate(algorithms):
        if dict['gd'][problem][algorithm][0] == 1:

            print '\cellcolor[HTML]{D1D5DE}',
            print r(dict['gd'][problem][algorithm][1]) ,'&',

        else:
            print r(dict['gd'][problem][algorithm][1]), ' &',

        if dict['igd'][problem][algorithm][0] == 1:
            print '\cellcolor[HTML]{D1D5DE}',
            print r(dict['igd'][problem][algorithm][1]),'&',
        else:
            print r(dict['igd'][problem][algorithm][1]), ' &',

        if dict['evals'][problem][algorithm][0] == 1:
            print '\cellcolor[HTML]{D1D5DE}',
            print dict['evals'][problem][algorithm][1],
        else:
            print dict['evals'][problem][algorithm][1],

        if i + 1 != len(algorithms): print '&',
    print '\\\ \cline{2-11}'
print "\multicolumn{2}{|c|}{\\textbf{Win (\%)}} &",

for i,algorithm in enumerate(algorithms):
    gd_wins = 0
    gd_losses = 0
    igd_wins = 0
    igd_losses = 0
    eval_losses = 0
    eval_wins = 0
    for problem in problems:
        if dict['gd'][problem][algorithm][0] == 1: gd_wins+=1
        else: gd_losses+=1

        if dict['igd'][problem][algorithm][0] == 1: igd_wins += 1
        else: igd_losses += 1

        if dict['evals'][problem][algorithm][0] == 1: eval_wins += 1
        else: eval_losses += 1

    print int((gd_wins * 100)/(gd_wins + gd_losses)), "&",
    print int((igd_wins * 100) / (igd_wins + igd_losses)), "&",
    print int((eval_wins * 100) / (eval_wins + eval_losses)),
    # print int((eval_wins * 100) / (eval_wins + eval_losses)),
    if i + 1 != len(algorithms): print '&',
print '\\\ \hline'