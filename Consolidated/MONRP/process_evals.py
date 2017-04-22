from __future__ import division
import pickle
import os
from sk import rdivDemo

pickle_files = [f for f in os.listdir(".") if ".py" not in f]
content = pickle.load(open(pickle_files[0]))
problems = content.keys()

prob = {}
for problem in problems:
    al2 = pickle.load(open('al2_monrp.p'))
    al = pickle.load(open('al_monrp.p'))
    mmre = pickle.load(open('mmre_monrp.p'))
    nsgaii = pickle.load(open('nsgaii_monrp.p'))
    rank = pickle.load(open('rank_monrp.p'))
    spea2 = pickle.load(open('spea2_monrp.p'))
    sway5 = pickle.load(open('SWAY5_monrp.p'))

    lists = list()
    lists.append(['AL2'] + al2[problem]['evals'])
    lists.append(['AL'] + al[problem]['evals'])
    lists.append(['MMRE'] + mmre[problem]['evals'])
    lists.append(['NSGAII'] + nsgaii[problem]['evals'])
    lists.append(['Rank'] + rank[problem]['evals'])
    lists.append(['SPEA2'] + spea2[problem]['evals'])
    lists.append(['SWAY5'] + sway5[problem]['evals'])

    rdivDemo( problem.replace('_', '\_'), "", lists, globalMinMax=False,
             isLatex=True)

