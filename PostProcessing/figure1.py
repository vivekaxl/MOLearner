import pickle
import numpy as np
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import container
import matplotlib.pyplot as plt

def process():
    folder = "./PickleLocker/"
    mmre = pickle.load(open(folder + "mmre-based.p"))
    rank = pickle.load(open(folder + "rank-based.p"))
    epal = pickle.load(open(folder + "epal.p"))

    files = mmre.keys()
    mmre_gd = []
    mmre_evals = []
    rank_gd = []
    rank_evals = []
    epal_gd_1 = []
    epal_evals_1 = []
    epal_gd_2 = []
    epal_evals_2 = []
    epal_gd_3 = []
    epal_evals_3 = []
    epal_gd_4 = []
    epal_evals_4 = []
    epal_gd_5 = []
    epal_evals_5 = []
    epal_gd_6 = []
    epal_evals_6 = []
    epal_gd_7 = []
    epal_evals_7 = []
    epal_gd_8 = []
    epal_evals_8 = []
    for file in files:
        mmre_gd.append(np.mean(mmre[file]['gen_dist']))
        mmre_evals.append(np.mean(mmre[file]['evals']))
        rank_gd.append(np.mean(rank[file]['gen_dist']))
        rank_evals.append(np.mean(rank[file]['evals']))

        epal_gd_1.append(np.mean(epal[file][0.01]['gen_dist']))
        epal_evals_1.append(np.mean(epal[file][0.01]['evals']))
        epal_gd_2.append(np.mean(epal[file][0.02]['gen_dist']))
        epal_evals_2.append(np.mean(epal[file][0.02]['evals']))
        epal_gd_3.append(np.mean(epal[file][0.04]['gen_dist']))
        epal_evals_3.append(np.mean(epal[file][0.04]['evals']))
        epal_gd_4.append(np.mean(epal[file][0.08]['gen_dist']))
        epal_evals_4.append(np.mean(epal[file][0.08]['evals']))
        epal_gd_5.append(np.mean(epal[file][0.12]['gen_dist']))
        epal_evals_5.append(np.mean(epal[file][0.12]['evals']))
        epal_gd_6.append(np.mean(epal[file][0.16]['gen_dist']))
        epal_evals_6.append(np.mean(epal[file][0.16]['evals']))
        epal_gd_7.append(np.mean(epal[file][0.2]['gen_dist']))
        epal_evals_7.append(np.mean(epal[file][0.2]['evals']))
        epal_gd_8.append(np.mean(epal[file][0.3]['gen_dist']))
        epal_evals_8.append(np.mean(epal[file][0.3]['evals']))

    arr = [1+7*i for i in xrange(len(files))]
    ind = np.array(arr)  # the x locations for the groups

    width = 0.5       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, mmre_gd, width/2, color='red')
    rects2 = ax.bar(ind+width, rank_gd, width/2, color='green')
    rects3 = ax.bar(ind+2*width, epal_gd_1, width/2)
    rects4 = ax.bar(ind+3*width, epal_gd_2, width/2)
    rects5 = ax.bar(ind+4*width, epal_gd_3, width/2)
    rects6 = ax.bar(ind+5*width, epal_gd_4, width/2)
    rects7 = ax.bar(ind+6*width, epal_gd_5, width/2)
    rects8 = ax.bar(ind+7*width, epal_gd_6, width/2)
    rects9 = ax.bar(ind+8*width, epal_gd_7, width/2)
    rects10 = ax.bar(ind+9*width, epal_gd_8, width/2)

    ax.set_xticks(ind + 3*width / 2)
    ax.set_xticklabels([file.split('/')[-1][:-4] for file in files], rotation=30)

    ax.set_ylabel('Generational Distance')
    plt.tight_layout()
    fig.set_size_inches(14, 5)
    # plt.show()
    plt.savefig('gd.png', bbox_inches='tight')


if __name__ == "__main__":
    process()