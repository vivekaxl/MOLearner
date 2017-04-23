from __future__ import division
import pickle
import os
from sk_table import rdivDemo

pickle_files = [f for f in os.listdir(".") if ".py" not in f]
content = pickle.load(open(pickle_files[0]))
# problems = content.keys()
problems = ['llvm_input.p', 'noc_CM_log.p', 'rs-6d-c3.p', 'sort_256.p', 'wc+rs-3d-c4.p', 'wc+sol-3d-c4.p', 'wc+wc-3d-c4.p', 'wc-3d-c4.p', 'wc-5d-c5.p', 'wc-6d-c1.p', 'wc-c1-3d-c1.p', 'wc-c3-3d-c1.p']

column_names = ["Name", "AL", "AL2", "MMRE", "Rank", "epal-0.01", "epal-0.02", "epal-0.04", "epal-0.08", "epal-0.16", "epal-0.20", "epal-0.30"]
return_string = ""
for column_name in column_names:
    if column_name == "Name":
        return_string += " \multicolumn{1}{|c|}{\\textbf{{" + column_name + "}}} & "
    else:
        return_string += " \multicolumn{1}{|c|}{\\textbf{\\rot{" + column_name + "}}} & "
return_string = return_string[:-2] + "\\\ \hline\n"
print return_string,

prob = {}
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
    try: lists.append(['AL2'] + al2[problem]['igd'])
    except: pass
    try: lists.append(['AL'] + al[problem]['igd'])
    except:
        pass
    try: lists.append(['MMRE'] + mmre[problem]['igd'])
    except:
        pass
    try: lists.append(['Rank'] + rank[problem]['igd'])
    except:
        pass
    try:lists.append(['epal\_0.01'] + epal_001[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.02'] + epal_002[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.04'] + epal_004[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.08'] + epal_008[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.16'] + epal_016[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.20'] + epal_020[problem]['igd'])
    except: pass
    try: lists.append(['epal\_0.30'] + epal_030[problem]['igd'])
    except: pass

    rdivDemo("SS" + str(i + 1), problem.replace('_', '\_'), lists, column_names, globalMinMax=False)

