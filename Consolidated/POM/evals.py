
from __future__ import division
import pickle
import os
from sk_table import rdivDemo


def get_gd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al = pickle.load(open('al_POM.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway5 = pickle.load(open('SWAY5_POM.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem+".p"]['gen_dist'])
        except:
            import pdb
            pdb.set_trace()
            pass
        # flash3 = pickle.load(open('Flash4.p'))
        # lists.append(['Flash4'] + flash3[problem + ".p"]['gen_dist'])
        # try:
        #     lists.append(['AL'] + al[problem]['gen_dist'])
        # except:
        #     pass
        # try:
        #     lists.append(['MMRE'] + mmre[problem]['evals'])
        # except:
        #     pass
        # try:
        #     lists.append(['Rank'] + rank[problem]['evals'])
        # except:
        #     pass
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

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
    return ret_dict


def get_igd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al = pickle.load(open('al_POM.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway5 = pickle.load(open('SWAY5_POM.p'))

        lists = list()
        try:
            lists.append(['AL2'] + al2[problem+".p"]['igd'])
        except:
            pass
        # try:
        #     lists.append(['AL'] + al[problem]['igd'])
        # except:
        #     pass
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

        ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists,globalMinMax=False)
    return ret_dict


def get_eval_rank(problems):
    return_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2_20_POM.p'))
        al = pickle.load(open('al_POM.p'))

        nsgaii = pickle.load(open('NSGAII_POM.p'))
        spea2 = pickle.load(open('SPEA2_POM.p'))
        sway = pickle.load(open('SWAY5_POM.p'))

        lists = list()
        try: lists.append(['AL2'] + al2[problem+".p"]['evals'])
        except: pass
        # flash3 = pickle.load(open('Flash4.p'))
        # lists.append(['Flash4'] + flash3[problem + ".p"]['evals'])
        # try: lists.append(['AL'] + al[problem]['evals'])
        # except:
        #     pass
        try:lists.append(['NSGAII'] + nsgaii[problem]['evals'])
        except: pass
        try: lists.append(['SPEA2'] + spea2[problem]['evals'])
        except: pass
        try: lists.append(['SWAY'] + sway[problem]['evals'])
        except: pass

        return_dict[problem] = rdivDemo("SS"+ str(i+1), problem.replace('_', '\_'), lists, globalMinMax=False)

    return return_dict

# dict = {}
# problems = ['POM3A', 'POM3B', 'POM3C', 'POM3D']
#
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
algorithms = [ 'AL2', 'NSGAII', 'SPEA2', 'SWAY']
problems = ['POM3A', 'POM3B', 'POM3C', 'POM3D']

all_evals = {}
for i, algorithm in enumerate(algorithms):
    temp = []
    for problem in problems:
        temp.append(dict['evals'][problem][algorithm][1])
    all_evals[algorithm] = temp

print all_evals['AL2']
print all_evals['NSGAII']
print all_evals['SPEA2']
print all_evals['SWAY']