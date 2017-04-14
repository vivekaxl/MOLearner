import pickle
import numpy as np
import sys
from sk import rdivDemo
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import container
import matplotlib.pyplot as plt
from matplotlib import rc
from sk import rdivDemo

def process():
    rc('text', usetex=True)
    folder = "./PickleLocker/"
    mmre = pickle.load(open(folder + "mmre-based.p"))
    rank = pickle.load(open(folder + "rank-based.p"))
    epal = pickle.load(open(folder + "epal.p"))
    al = pickle.load(open(folder + "al-based.p"))
    al_2 = pickle.load(open(folder + "al-based-2.p"))
    al_3 = pickle.load(open(folder + "al-based-3.p"))
    pop0 = pickle.load(open(folder + "pop0-based.p"))

    files = mmre.keys()
    for i, file in enumerate(sorted(files)):
        lists = list()
        # lists.append(["MMRE-Prog"] + mmre[file]['igd'])
        # lists.append(["Rank-Prog"] + rank[file]['igd'])

        lists.append(["ePAL-0.01"] + epal[file][0.01]['igd'])
        lists.append(["ePAL-0.02"] + epal[file][0.02]['igd'])
        lists.append(["ePAL-0.04"] + epal[file][0.04]['igd'])
        lists.append(["ePAL-0.08"] + epal[file][0.08]['igd'])
        lists.append(["ePAL-0.12"] + epal[file][0.12]['igd'])
        lists.append(["ePAL-0.16"] + epal[file][0.16]['igd'])
        lists.append(["ePAL-0.2"] + epal[file][0.2]['igd'])
        lists.append(["ePAL-0.3"] + epal[file][0.3]['igd'])

        lists.append(["AL1"] + al[file]['igd'])
        lists.append(["\hl{AL2}"] + al_2[file]['igd'])
        lists.append(["AL3"] + al_3[file]['igd'])
        lists.append(["\colorbox{blue}{pop0}"] + pop0[file]['igd'])

        rdivDemo("SS" + str(i + 1),file.split('/')[-1].split('.')[0].replace('_', '\_'), lists, globalMinMax=False, isLatex=True)




process()