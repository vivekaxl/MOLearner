import os

files = [
    './Data/llvm_input.csv',
    './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.csv',
    './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.csv',
    './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.csv',
    './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.csv',
    './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.csv',
    './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.csv',
    './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.csv',
    './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.csv',
    './Data/noc_CM_log.csv',
    './Data/POM3A-p10000-d9-o3-dataset1.csv',
    './Data/POM3A-p10000-d9-o3-dataset2.csv',
    './Data/POM3B-p10000-d9-o3-dataset1.csv',
    './Data/POM3B-p10000-d9-o3-dataset2.csv',
    './Data/POM3C-p10000-d9-o3-dataset1.csv',
    './Data/POM3C-p10000-d9-o3-dataset2.csv',
    './Data/POM3D-p10000-d9-o3-dataset1.csv',
    './Data/POM3D-p10000-d9-o3-dataset2.csv',
    './Data/rs-6d-c3.csv',
    './Data/SaC1_2.csv',
    './Data/SaC_11_12.csv',
    './Data/SaC_3_4.csv',
    './Data/SaC_5_6.csv',
    './Data/SaC_7_8.csv',
    './Data/SaC_9_10.csv',
    './Data/sol-6d-c2.csv',
    './Data/sort_256.csv',
    './Data/TriMesh_1_2.csv',
    './Data/TriMesh_2_3.csv',
    './Data/wc+rs-3d-c4.csv',
    './Data/wc+sol-3d-c4.csv',
    './Data/wc+wc-3d-c4.csv',
    './Data/wc-3d-c4.csv',
    './Data/wc-5d-c5.csv',
    './Data/wc-6d-c1.csv',
    './Data/wc-c1-3d-c1.csv',
    './Data/wc-c3-3d-c1.csv',
    './Data/x264-DB_1_2.csv',
    './Data/x264-DB_2_3.csv',
    './Data/x264-DB_3_4.csv',
    './Data/x264-DB_4_5.csv',
    './Data/x264-DB_5_6.csv',
    './Data/xomo_all-p10000-d27-o4-dataset1.csv',
    './Data/xomo_all-p10000-d27-o4-dataset2.csv',
    './Data/xomo_all-p10000-d27-o4-dataset3.csv',
    './Data/xomo_flight-p10000-d27-o4-dataset1.csv',
    './Data/xomo_flight-p10000-d27-o4-dataset2.csv',
    './Data/xomo_flight-p10000-d27-o4-dataset3.csv',
    './Data/xomo_ground-p10000-d27-o4-dataset1.csv',
    './Data/xomo_ground-p10000-d27-o4-dataset2.csv',
    './Data/xomo_ground-p10000-d27-o4-dataset3.csv',
    './Data/xomo_osp-p10000-d27-o4-dataset1.csv',
    './Data/xomo_osp-p10000-d27-o4-dataset2.csv',
    './Data/xomo_osp-p10000-d27-o4-dataset3.csv',
    './Data/xomoo2-p10000-d27-o4-dataset1.csv',
    './Data/xomoo2-p10000-d27-o4-dataset2.csv',
    './Data/xomoo2-p10000-d27-o4-dataset3.csv',
]

main_file = "active_learner.py"
for file in files:
    filename = file.split('/')[-1].split(".")[0]
    # cmd = "cp " + main_file + " " + "AL1_" + filename + ".py"
    content = open(main_file).readlines()
    content[217] = content[217].replace('files = []', 'files = [\'./Data/' + filename + '.csv\']')
    content[-1] = content[-1].replace('al-based-3.p', 'al3-' + filename + '.p')

    thefile = open("al1-" + filename + ".py", 'w')
    for item in content:
        thefile.write("%s\n" % item)