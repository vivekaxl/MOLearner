
from __future__ import division
import pickle
import os
from sk_table import rdivDemo


def get_gd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate((problems)):
        print problem
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))

        # import pdb
        # pdb.set_trace()
        lists = list()
        epal = pickle.load(open('epal_2.p'))
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.01'] + epal['./Data/x264-DB_2_3.csv'][0.01]['gen_dist'])
            else:
                lists.append(['epal\_0.01'] + epal[problem][0.01]['gen_dist'])
        except: pass
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.3'] + epal['./Data/x264-DB_2_3.csv'][0.3]['gen_dist'])
            else:
                lists.append(['epal\_0.3'] + epal[problem][0.3]['gen_dist'])
        except:
            pass
        try:
            lists.append(['AL2'] + al2[problem]['gen_dist'])
        except:
            pass
        # try:
        #     lists.append(['AL'] + al[problem]['gen_dist'])
        # except:
        #     pass
        print len(lists)
        if len(lists) != 0: # only the name
            ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
        else:
            table_dict = {}
            ret_dict[problem] = table_dict['AL2'] = [-1, -1]

    return ret_dict


def get_igd_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))


        lists = list()
        lists = list()
        epal = pickle.load(open('epal_2.p'))
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.01'] + epal['./Data/x264-DB_2_3.csv'][0.01]['igd'])
            else:
                lists.append(['epal\_0.01'] + epal[problem][0.01]['igd'])
        except: pass
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.3'] + epal['./Data/x264-DB_2_3.csv'][0.3]['igd'])
            else:
                lists.append(['epal\_0.3'] + epal[problem][0.3]['igd'])
        except:
            pass

        try:
            lists.append(['AL2'] + al2[problem]['igd'])
        except:
            pass
        # try:
        #     lists.append(['AL'] + al[problem]['igd'])
        # except:
        #     pass


        if len(lists) != 0: # only the name
            ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
        else:
            table_dict = {}
            ret_dict[problem] = table_dict['AL2'] = [-1, -1]
    return ret_dict


def get_eval_rank(problems):
    ret_dict = {}
    for i, problem in enumerate(sorted(problems)):
        al2 = pickle.load(open('al2-based_Config.p'))
        al = pickle.load(open('al-based_Config.p'))

        lists = list()
        epal = pickle.load(open('epal_2.p'))
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.01'] + epal['./Data/x264-DB_2_3.csv'][0.01]['evals'])
            else:
                lists.append(['epal\_0.01'] + epal[problem][0.01]['evals'])
        except: pass
        try:
            if problem == 'x264-DB_2_3.p':
                lists.append(['epal\_0.3'] + epal['./Data/x264-DB_2_3.csv'][0.3]['evals'])
            else:
                lists.append(['epal\_0.3'] + epal[problem][0.3]['evals'])
        except:
            pass

        try: lists.append(['AL2'] + al2[problem]['evals'])
        except: pass
        # try: lists.append(['AL'] + al[problem]['evals'])
        # except:
        #     pass

        if len(lists) != 0: # only the name
            ret_dict[problem] = rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, globalMinMax=False)
        else:
            table_dict = {}
            ret_dict[problem] = table_dict['AL2'] = [-1, -1]

    return ret_dict

dict = {}
problems = ['x264-DB_2_3.p', 'SaC1_2.p', 'SaC_11_12.p', 'SaC_3_4.p', 'SaC_5_6.p', 'SaC_7_8.p', 'SaC_9_10.p', 'TriMesh_1_2.p', 'TriMesh_2_3.p', 'x264-DB_1_2.p',  'x264-DB_3_4.p', 'x264-DB_4_5.p', 'x264-DB_5_6.p']
dict['gd'] = get_gd_rank(problems)
dict['igd'] = get_igd_rank(problems)
dict['evals'] = get_eval_rank(problems)

assert(len(dict['gd'].keys()) == len(dict['igd'].keys())), "Something is wrong"
assert(len(dict['gd'].keys()) == len(dict['evals'].keys())), "Something is wrong"

pickle.dump(dict, open('stat_result.p', 'w'))

def r(data): return round(data, 2)
dict = pickle.load(open('stat_result.p'))

columns_dict = {'sort_256': 3, 'wc-c3-3d-c1': 3, 'reduced_TriMesh_2_3': 9, 'SaC_11_12': 59, 'x264-DB_4_5': 17,
                'noc_CM_log': 4, 'x264-DB_5_6': 17, 'x264-DB_2_3': 17, 'x264-DB_3_4': 17, 'x264-DB': 17,
                'reduced_TriMesh_1_2': 9, 'wc-6d-c1': 6, 'TriMesh': 13, 'SaC1_2': 59, 'wc-c1-3d-c1': 3,
                'wc-5d-c5': 5, 'x264-DB_1_2': 17, 'SaC': 59, 'sol-6d-c2': 6, 'wc+wc-3d-c4': 3, 'SaC_7_8': 59,
                'TriMesh_1_2': 13, 'wc-3d-c4': 3, 'SaC_9_10': 59, 'wc+rs-3d-c4': 3, 'SaC_5_6': 59, 'rs-6d-c3': 6,
                'llvm_input': 11, 'wc+sol-3d-c4': 3, 'TriMesh_2_3': 13, 'SaC_3_4': 59}

algorithms = ['AL2', 'epal0.01', 'epal0.3']
# problems = ['SaC1_2.p', 'SaC_11_12.p', 'SaC_3_4.p', 'SaC_5_6.p', 'SaC_7_8.p', 'SaC_9_10.p', 'TriMesh_1_2.p', 'TriMesh_2_3.p', 'x264-DB_1_2.p', 'x264-DB_2_3.p',  'x264-DB_3_4.p', 'x264-DB_4_5.p', 'x264-DB_5_6.p']
problems = ['SaC1_2.p', 'TriMesh_1_2.p',  'x264-DB_2_3.p', ]
header = "\multirow{3}{*}{\\textbf{Name}} & \multirow{3}{*}{\\textbf{\\rot{\# Decisions}}}& \multicolumn{3}{c|}{\multirow{2}{*}{\\textbf{FLASH}}} & \multicolumn{15}{c|}{\\textbf{ePAL}}                                                                     \\\ \cline{6-20}\n"
header += "& & \multicolumn{3}{c|}{} & \multicolumn{3}{c|}{\\textbf{ePal-0.01}} & \multicolumn{3}{c|}{\\textbf{ePal-0.04}} &  \multicolumn{3}{c|}{\\textbf{ePal-0.12}}  & \multicolumn{3}{c|}{\\textbf{ePal-0.20}} & \multicolumn{3}{c|}{\\textbf{ePal-0.30}} \\\ \cline{3-20} \n"
header += " & & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} &\\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} & \\rot{GD} & \\rot{IGD} & \\rot{Evals} \\\ \hline"
print header
for problem in problems:
    print problem.replace('_', '\_'), '&', columns_dict[problem[:-2]], '&',
    for i, algorithm in enumerate(algorithms):
        try:
            if dict['gd'][problem][algorithm][0] == 1: print '\cellcolor[HTML]{D1D5DE}', int(r(dict['gd'][problem][algorithm][1])/r(dict['gd'][problem]['AL2'][1]) * 100) ,'&',
            else: print int(r(dict['gd'][problem][algorithm][1])/r(dict['gd'][problem]['AL2'][1]) * 100), ' &',
        except:
            try:
                if dict['gd'][problem]['AL2'][1] == 0: print " 100 &",
                else:
                    print " x &",
            except:
                print " x &",

        try:
            if dict['igd'][problem][algorithm][0] == 1: print '\cellcolor[HTML]{D1D5DE}', int(r(dict['igd'][problem][algorithm][1])/r(dict['igd'][problem]['AL2'][1]) * 100),
            else: print int(r(dict['igd'][problem][algorithm][1])/r(dict['igd'][problem]['AL2'][1]) * 100),
        except:
            print " x ",
        # try:
        #     if dict['evals'][problem][algorithm][0] == 1: print '\cellcolor[HTML]{D1D5DE}', int(dict['evals'][problem][algorithm][1]),
        #     else: print int(dict['evals'][problem][algorithm][1]),
        # except:
        #     print "x",
        if i + 1 != len(algorithms): print '&',
    print '\\\ \hline'
print "\multicolumn{2}{|c|}{\\textbf{Win (\%)}}",


for i,algorithm in enumerate(algorithms):
    gd_wins = 0
    gd_losses = 0
    igd_wins = 0
    igd_losses = 0
    eval_losses = 0
    eval_wins = 0
    for problem in problems:
        try:
            if dict['gd'][problem][algorithm][0] == 1: gd_wins+=1
            else: gd_losses+=1


            if dict['igd'][problem][algorithm][0] == 1: igd_wins += 1
            else: igd_losses += 1


            if dict['evals'][problem][algorithm][0] == 1: eval_wins += 1
            else: eval_losses += 1
        except:
            gd_losses +=1
            igd_losses += 1
            eval_losses += 1
            pass

    try:
        print int((gd_wins * 100)/(gd_wins + gd_losses)), "&",
    except:
        print "0 &",
    try:
        print int((igd_wins * 100) / (igd_wins + igd_losses)), "&",
    except:
        print "0 &",
    try:
        print int((eval_wins * 100) / (eval_wins + eval_losses)),
    except:
        print "0",
    if i + 1 != len(algorithms): print '&',
print '\\\ \hline'

# import pdb
# pdb.set_trace(&