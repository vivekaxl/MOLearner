from __future__ import division
import pickle
import os
from sk import rdivDemo

pickle_files = [f for f in os.listdir(".") if ".py" not in f]
content = pickle.load(open(pickle_files[0]))
problems = content.keys()

prob = {}
for problem in problems:
    al2 = pickle.load(open('al2_XOMO.p'))
    al = pickle.load(open('al_XOMO.p'))
    mmre = pickle.load(open('mmre_XOMO.p'))
    nsgaii = pickle.load(open('nsgaii_XOMO.p'))
    rank = pickle.load(open('rank_XOMO.p'))
    spea2 = pickle.load(open('spea2_XOMO.p'))
    sway5 = pickle.load(open('SWAY5_XOMO.p'))

    lists = list()
    lists.append(['AL2'] + al2[problem]['igd'])
    lists.append(['AL'] + al[problem]['igd'])
    lists.append(['MMRE'] + mmre[problem]['igd'])
    lists.append(['NSGAII'] + nsgaii[problem]['igd'])
    lists.append(['Rank'] + rank[problem]['igd'])
    lists.append(['SPEA2'] + spea2[problem]['igd'])
    lists.append(['SWAY5'] + sway5[problem]['igd'])

    rdivDemo( problem.replace('_', '\_'), "", lists, globalMinMax=False,
             isLatex=True)

