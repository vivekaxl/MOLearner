import os

files = [
 './Data/reduced_SaC1_2.csv',
 './Data/reduced_SaC_11_12.csv',
 './Data/reduced_SaC_3_4.csv',
 './Data/reduced_SaC_5_6.csv',
 './Data/reduced_SaC_7_8.csv',
 './Data/reduced_SaC_9_10.csv',
 './Data/reduced_TriMesh_1_2.csv',
 './Data/reduced_TriMesh_2_3.csv',
 './Data/reduced_x264-DB_1_2.csv',
 './Data/reduced_x264-DB_2_3.csv',
 './Data/reduced_x264-DB_3_4.csv',
 './Data/reduced_x264-DB_4_5.csv',
 './Data/reduced_x264-DB_5_6.csv',
 './Data/llvm_input.csv',
 './Data/noc_CM_log.csv',
 './Data/rs-6d-c3.csv',
 './Data/sol-6d-c2.csv',
 './Data/sort_256.csv',
 './Data/wc+rs-3d-c4.csv',
 './Data/wc+sol-3d-c4.csv',
 './Data/wc+wc-3d-c4.csv',
 './Data/wc-3d-c4.csv',
 './Data/wc-5d-c5.csv',
 './Data/wc-6d-c1.csv',
 './Data/wc-c1-3d-c1.csv',
 './Data/wc-c3-3d-c1.csv',]

main_file = "active_learner_3.py"
for file in files:
    filename = file.split('/')[-1].split(".")[0]
    # cmd = "cp " + main_file + " " + "AL1_" + filename + ".py"
    content = open(main_file).readlines()
    content[217] = content[217].replace('files = []', 'files = [\'./Data/' + filename + '.csv\']')
    content[-1] = content[-1].replace('al-based-3.p', 'al3-' + filename + '.p')

    thefile = open("al3-" + filename + ".py", 'w')
    for item in content:
        thefile.write("%s\n" % item)