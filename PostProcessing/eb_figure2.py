import pickle
import numpy as np
import sys
sys.path.append("/Users/viveknair/GIT/MOLearner/")
from utility import container
import matplotlib.pyplot as plt
from matplotlib import rc


def get_iqr(x):
    return np.subtract(*np.percentile(x, [75, 25]))


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
    std_epal_gd_mmre = []
    rank_gd = []
    std_epal_gd_rank = []
    mean_epal_gd_1 = []
    std_epal_gd_1 = []
    mean_epal_gd_2 = []
    std_epal_gd_2 = []
    mean_epal_gd_3 = []
    std_epal_gd_3 = []
    mean_epal_gd_4 = []
    std_epal_gd_4 = []
    mean_epal_gd_5 = []
    std_epal_gd_5 = []
    mean_epal_gd_6 = []
    std_epal_gd_6 = []
    mean_epal_gd_7 = []
    std_epal_gd_7 = []
    mean_epal_gd_8 = []
    std_epal_gd_8 = []
    al_gd = []
    std_epal_gd_al = []
    al2_gd = []
    std_epal_gd_al2 = []
    al3_gd = []
    std_epal_gd_al3 = []

    for file in sorted(files):
        mmre_gd.append(np.median(mmre[file]['evals']))
        std_epal_gd_mmre.append(get_iqr(mmre[file]['evals']))
        rank_gd.append(np.median(rank[file]['evals']))
        std_epal_gd_rank.append(get_iqr(mmre[file]['evals']))

        mean_epal_gd_1.append(np.median(epal[file][0.01]['evals']))
        std_epal_gd_1.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_2.append(np.median(epal[file][0.02]['evals']))
        std_epal_gd_2.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_3.append(np.median(epal[file][0.04]['evals']))
        std_epal_gd_3.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_4.append(np.median(epal[file][0.08]['evals']))
        std_epal_gd_4.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_5.append(np.median(epal[file][0.12]['evals']))
        std_epal_gd_5.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_6.append(np.median(epal[file][0.16]['evals']))
        std_epal_gd_6.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_7.append(np.median(epal[file][0.2]['evals']))
        std_epal_gd_7.append(get_iqr(epal[file][0.01]['evals']))
        mean_epal_gd_8.append(np.median(epal[file][0.3]['evals']))
        std_epal_gd_8.append(get_iqr(epal[file][0.01]['evals']))

        al_gd.append(np.median(al[file]['evals']))
        std_epal_gd_al.append(get_iqr(al[file]['evals']))

        al2_gd.append(np.median(al_2[file]['evals']))
        std_epal_gd_al2.append(get_iqr(al_2[file]['evals']))

        al3_gd.append(np.median(al_3[file]['evals']))
        std_epal_gd_al3.append(get_iqr(al_3[file]['evals']))


    arr = [1+9*i for i in xrange(len(files))]
    ind = np.array(arr)  # the x locations for the groups

    width = 0.5       # the width of the bars

    fig, ax = plt.subplots()

    rects3 = ax.errorbar(ind + 0 * width, mean_epal_gd_1, std_epal_gd_1, label=r"epal\-0.01", color="#79CDCD", fmt='o',
                         markersize=2)
    rects4 = ax.errorbar(ind + 1 * width, mean_epal_gd_2, std_epal_gd_2, label=r"epal\-0.02", color="#66CCCC", fmt='o',
                         markersize=2)
    rects5 = ax.errorbar(ind + 2 * width, mean_epal_gd_3, std_epal_gd_3, label=r"epal\-0.04", color="#AEEEEE", fmt='o',
                         markersize=2)
    rects6 = ax.errorbar(ind + 3 * width, mean_epal_gd_4, std_epal_gd_4, label=r"epal\-0.08", color="#37FDFC", fmt='o',
                         markersize=2)
    rects7 = ax.errorbar(ind + 4 * width, mean_epal_gd_5, std_epal_gd_5, label=r"epal\-0.12", color="#00CDCD", fmt='o',
                         markersize=2)
    rects8 = ax.errorbar(ind + 5 * width, mean_epal_gd_6, std_epal_gd_6, label=r"epal\-0.16", color="#00FFFF", fmt='o',
                         markersize=2)
    rects9 = ax.errorbar(ind + 6 * width, mean_epal_gd_7, std_epal_gd_7, label=r"epal\-0.20", color="#E0FFFF", fmt='o',
                         markersize=2)
    rects10 = ax.errorbar(ind + 7 * width, mean_epal_gd_8, std_epal_gd_8, label=r"epal\-0.3", color="#00E5EE", fmt='o',
                          markersize=2)
    # rects11 = ax.errorbar(ind + 8 * width, mmre_gd, std_epal_gd_mmre, color='red', label="mmre-prog", fmt='o',
    #                       markersize=2)
    rects12 = ax.errorbar(ind + 9 * width, rank_gd, std_epal_gd_rank, color='green', label="rank-prog", fmt='o',
                          markersize=2)
    rects12 = ax.errorbar(ind + 10 * width, al_gd, std_epal_gd_al, color='yellow', label="AL1", fmt='o', markersize=2)
    rect13 = ax.errorbar(ind + 11 * width, al2_gd, std_epal_gd_al2, color='orange', label=r"\textbf{AL2}", fmt='o',
                         markersize=4)
    rect14 = ax.errorbar(ind + 12 * width, al3_gd, std_epal_gd_al3, color='black', label=r"AL3", fmt='o', markersize=2)

    ax.set_xticks(ind + 3*width / 2)
    ax.set_xticklabels([r"$"+str(file.split('/')[-1][:-4] + "$")  for file in sorted(files)], rotation=30)
    ax.legend(frameon=False, loc='upper center',
              bbox_to_anchor=(0.5, -0.15),fancybox=True, ncol=6)

    ax.set_ylabel('Evaluations')
    plt.tight_layout()
    fig.set_size_inches(14, 5)
    # plt.show()
    plt.savefig('evals_al_errorbar1.png', bbox_inches='tight')


if __name__ == "__main__":
    process()