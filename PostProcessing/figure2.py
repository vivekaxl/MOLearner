import pickle
import numpy as np
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import container
import matplotlib.pyplot as plt
from matplotlib import rc

def process():
    rc('text', usetex=True)
    folder = "./PickleLocker/"
    mmre = pickle.load(open(folder + "mmre-based.p"))
    rank = pickle.load(open(folder + "rank-based.p"))
    epal = pickle.load(open(folder + "epal.p"))
    al = pickle.load(open(folder + "al-based.p"))
    al_2 = pickle.load(open(folder + "al-based-2.p"))
    al_3 = pickle.load(open(folder + "al-based-3.p"))

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
    al_gd = []
    al_evals = []
    al2_gd = []
    al2_evals = []
    al3_gd = []
    al3_evals = []

    for file in sorted(files):
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

        al_gd.append(np.mean(al[file]['gen_dist']))
        al_evals.append(np.mean(al[file]['evals']))

        al2_gd.append(np.mean(al_2[file]['gen_dist']))
        al2_evals.append(np.mean(al_2[file]['evals']))

        al3_gd.append(np.mean(al_3[file]['gen_dist']))
        al3_evals.append(np.mean(al_3[file]['evals']))


    arr = [1+7*i for i in xrange(len(files))]
    ind = np.array(arr)  # the x locations for the groups

    width = 0.5       # the width of the bars

    fig, ax = plt.subplots()

    rects3 = ax.bar(ind+0*width, epal_evals_1, width/2,log=True, label=r"epal\-0.01", color="#79CDCD")
    rects4 = ax.bar(ind+1*width, epal_evals_2, width/2,log=True, label=r"epal\-0.02", color="#66CCCC")
    rects5 = ax.bar(ind+2*width, epal_evals_3, width/2,log=True, label=r"epal\-0.04", color="#AEEEEE")
    rects6 = ax.bar(ind+3*width, epal_evals_4, width/2,log=True, label=r"epal\-0.08", color="#37FDFC")
    rects7 = ax.bar(ind+4*width, epal_evals_5, width/2,log=True, label=r"epal\-0.12", color="#00CDCD")
    rects8 = ax.bar(ind+5*width, epal_evals_6, width/2,log=True, label=r"epal\-0.16", color="#00FFFF")
    rects9 = ax.bar(ind+6*width, epal_evals_7, width/2,log=True, label=r"epal\-0.20", color="#E0FFFF")
    rects10 = ax.bar(ind+7*width, epal_evals_8, width/2,log=True, label=r"epal\-0.3", color="#00E5EE")
    rects11 = ax.bar(ind+8*width, mmre_evals, width/2,log=True, color='red', label="mmre-prog")
    rects12 = ax.bar(ind+9*width, rank_evals, width/2,log=True, color='green', label="rank-prog")
    rects13 = ax.bar(ind+10*width, al_evals, width/2,log=True, color='yellow', label="AL1")
    rect14 = ax.bar(ind+11*width, al2_evals, width/2, color='orange', label=r"\textbf{AL2}")
    rect14 = ax.bar(ind + 12 * width, al3_evals, width / 2, color='black', label=r"AL3")


    ax.set_xticks(ind + 3*width / 2)
    ax.set_xticklabels([r"$"+str(file.split('/')[-1][:-4] + "$")  for file in sorted(files)], rotation=30)
    ax.legend(frameon=False, loc='upper center',
              bbox_to_anchor=(0.5, -0.15),fancybox=True, ncol=6)

    ax.set_ylabel('Evaluations')
    plt.tight_layout()
    fig.set_size_inches(14, 5)
    # plt.show()
    plt.savefig('evals_al3.png', bbox_inches='tight')


if __name__ == "__main__":
    process()