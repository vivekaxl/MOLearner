from __future__ import division
import pickle
import os
from sk import rdivDemo

pickle_files = [f for f in os.listdir(".") if ".py" not in f]
content = pickle.load(open(pickle_files[0]))
problems = content.keys()

prob = {}
for problem in problems:
    al2 = pickle.load(open('al2_POM.p'))
    al = pickle.load(open('al_POM.p'))
    mmre = pickle.load(open('mmre_POM.p'))
    nsgaii = pickle.load(open('nsgaii_POM.p'))
    rank = pickle.load(open('rank_POM.p'))
    spea2 = pickle.load(open('spea2_POM.p'))
    sway5 = pickle.load(open('SWAY5_POM.p'))

    lists = list()
    lists.append(['AL2'] + al2[problem]['gen_dist'])
    lists.append(['AL'] + al[problem]['gen_dist'])
    lists.append(['MMRE'] + mmre[problem]['gen_dist'])
    lists.append(['NSGAII'] + nsgaii[problem]['gen_dist'])
    lists.append(['Rank'] + rank[problem]['gen_dist'])
    lists.append(['SPEA2'] + spea2[problem]['gen_dist'])
    lists.append(['SWAY5'] + sway5[problem]['gen_dist'])

    rdivDemo( problem.replace('_', '\_'), "", lists, globalMinMax=False,
             isLatex=True)

