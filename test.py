from utility import read_file
from non_dominated_sort_fast import non_dominated_sort_fast
import sys

if __name__ == "__main__":
    files = [
        './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset1.csv',
        './Data/MONRP_50_4_5_0_110-p10000-d50-o3-dataset2.csv',
        './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset1.csv',
        './Data/MONRP_50_4_5_0_90-p10000-d50-o3-dataset2.csv',
        './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset1.csv',
        './Data/MONRP_50_4_5_4_110-p10000-d50-o3-dataset2.csv',
        './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset1.csv',
        './Data/MONRP_50_4_5_4_90-p10000-d50-o3-dataset2.csv',
        './Data/POM3A-p10000-d9-o3-dataset1.csv',
        './Data/POM3A-p10000-d9-o3-dataset2.csv',
        './Data/POM3B-p10000-d9-o3-dataset1.csv',
        './Data/POM3B-p10000-d9-o3-dataset2.csv',
        './Data/POM3C-p10000-d9-o3-dataset1.csv',
        './Data/POM3C-p10000-d9-o3-dataset2.csv',
        './Data/POM3D-p10000-d9-o3-dataset1.csv',
        './Data/POM3D-p10000-d9-o3-dataset2.csv',
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

# Create 2 objectives
# import pandas as pd
#
# for file in files:
#     c1 = ['<$f1', '<$f2']
#     c2 = ['<$f2', '<$f3']
#     # c3 = ['<$f3', '<$f4']
#
#
#     content = pd.read_csv(file)
#     columns = content.columns
#     independent = [c for c in columns if "<$" not in c]
#     dependent = [c for c in columns if "<$"  in c]
#
#     first_columns = content[independent + c1]
#     second_columns = content[independent + c2]
#     # third_columns = content[independent + c3]
#
#     first_columns.to_csv(file[:-4] + "1.csv", index=False)
#     second_columns.to_csv(file[:-4] + "2.csv", index=False)
#     # third_columns.to_csv(file[:-4] + "3.csv", index=False)
#     print file

# for lessismore
# for file in files:
#     print "lessismore[\'"+ file + "\'] = [True, True]"

# for Ranges
# for file in files:
#     data = read_file(file)
#     objectives = [d.objectives for d in data]
#     obj1 = [o[0] for o in objectives]
#     obj2 = [o[1] for o in objectives]
#     print "ranges[\'" + file + "\'] = [[" + str(min(obj1)) + "," + str(max(obj1)) + '],[' + str(min(obj2)) + "," + str(max(obj2)) + ']]'

# get rid of the last 3 lines
for file in files:
    content = open(file).readlines()
    content = content[:-1]
    print file
    thefile = open(file, 'w')
    for item in content:
        thefile.write("%s" % item)
    thefile.close()
