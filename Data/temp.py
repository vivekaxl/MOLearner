import pandas as pd

files = [
 'reduced_SaC1_2.csv',
 'reduced_SaC_11_12.csv',
 'reduced_SaC_3_4.csv',
 'reduced_SaC_5_6.csv',
 'reduced_SaC_7_8.csv',
 'reduced_SaC_9_10.csv',
 'reduced_TriMesh_1_2.csv',
 'reduced_TriMesh_2_3.csv',
 'reduced_x264-DB_1_2.csv',
 'reduced_x264-DB_2_3.csv',
 'reduced_x264-DB_3_4.csv',
 'reduced_x264-DB_4_5.csv',
 'reduced_x264-DB_5_6.csv',
 'llvm_input.csv',
 'noc_CM_log.csv',
 'rs-6d-c3.csv',
 'sol-6d-c2.csv',
 'sort_256.csv',
 'wc+rs-3d-c4.csv',
 'wc+sol-3d-c4.csv',
 'wc+wc-3d-c4.csv',
 'wc-3d-c4.csv',
 'wc-5d-c5.csv',
 'wc-6d-c1.csv',
 'wc-c1-3d-c1.csv',
 'wc-c3-3d-c1.csv',]


for file in files:
    strg = "ranges[\"" + file + "\"] = ["
    data = pd.read_csv(file)
    dependent_cols = [c for c in data.columns if '<$' in c]
    strg += "[" + str(min(data[dependent_cols[0]])) + ", " + str(max(data[dependent_cols[0]])) + "],"
    strg += "[" + str(min(data[dependent_cols[1]])) + ", " + str(max(data[dependent_cols[1]])) + "]]"
    print strg