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
    content = pickle.load(open("./consolidated_result.p"))
    problems = [
        # '_wc-3d-c4.p',
        # 'llvm_input.p',
        # 'noc_CM_log.p',
        # 'rs-6d-c3.p',
        # 'sort_256.p',
        # 'wc+rs-3d-c4.p',
        # 'wc+sol-3d-c4.p',
        # 'wc+wc-3d-c4.p',
        # 'wc-5d-c5.p',
        # 'wc-6d-c1.p',
        # 'wc-c1-3d-c1.p',
        # 'wc-c3-3d-c1.p',
        #
        # 'SaC1_2.p',
        'SaC_11_12.p',
        # 'SaC_3_4.p',
        # 'SaC_5_6.p',
        # 'SaC_9_10.p',
        #
        # 'x264-DB_1_2.p',
        # 'x264-DB_2_3.p',
        # 'x264-DB_3_4.p',
        # 'x264-DB_4_5.p',
        # 'x264-DB_5_6.p',
        #
        # 'POM3A-p10000-d9-o3-dataset1.p',
        # 'POM3A-p10000-d9-o3-dataset2.p',
        # 'POM3B-p10000-d9-o3-dataset1.p',
        # 'POM3B-p10000-d9-o3-dataset2.p',
        # 'POM3C-p10000-d9-o3-dataset1.p',
        # 'POM3C-p10000-d9-o3-dataset2.p',
        # 'POM3D-p10000-d9-o3-dataset1.p',
        # 'POM3D-p10000-d9-o3-dataset2.p',
        #
        # 'xomo_all-p10000-d27-o4-dataset1.p',
        # 'xomo_all-p10000-d27-o4-dataset2.p',
        # 'xomo_all-p10000-d27-o4-dataset3.p',
        # 'xomo_flight-p10000-d27-o4-dataset1.p',
        # 'xomo_flight-p10000-d27-o4-dataset2.p',
        # 'xomo_flight-p10000-d27-o4-dataset3.p',
        # 'xomo_ground-p10000-d27-o4-dataset1.p',
        # 'xomo_ground-p10000-d27-o4-dataset2.p',
        # 'xomo_ground-p10000-d27-o4-dataset3.p',
        # 'xomo_osp-p10000-d27-o4-dataset1.p',
        # 'xomo_osp-p10000-d27-o4-dataset2.p',
        # 'xomo_osp-p10000-d27-o4-dataset3.p',
        # 'xomoo2-p10000-d27-o4-dataset1.p',
        # 'xomoo2-p10000-d27-o4-dataset2.p',
        # 'xomoo2-p10000-d27-o4-dataset3.p',
        #
        # 'MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.p',
        # 'MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.p',
        # 'MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.p',
        # 'MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.p',
        # 'MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.p',
        # 'MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.p',
        # 'MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.p',
        # 'MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.p',



    ]
    count = 0
    for problem in problems:
        if count in [45, 30, 22, 17, 12]:
            print "\\newpage"

        count += 1
        problem_content = content[problem]
        lists = list()
        lists.append(['AL1'] + problem_content['al1']['gen_dist'])
        lists.append(['AL2'] + problem_content['al2']['gen_dist'])
        lists.append(['MMRE'] + problem_content['mmre']['gen_dist'])
        lists.append(['Rank'] + problem_content['rank']['gen_dist'])
        import pdb
        pdb.set_trace()
        name = problem.replace('_', '\_').replace('-p10000-d27-o4-dataset', '-')
        name = name.replace('-p10000-d9-o3-dataset', '-').replace('-p10000-d50-o3-dataset', '-')
        rdivDemo(name, "", lists, globalMinMax=False, isLatex=True)


process()