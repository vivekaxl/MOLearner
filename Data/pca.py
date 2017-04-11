from sklearn.decomposition import PCA
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# files = [f for f in os.listdir('.') if ".csv" in f]
files = ["TriMesh_1_2.csv", "TriMesh_2_3.csv", "SaC1_2.csv", "SaC_11_12.csv", "SaC_3_4.csv", "SaC_5_6.csv", "SaC_7_8.csv", "SaC_9_10.csv", "x264-DB_1_2.csv", "x264-DB_2_3.csv", "x264-DB_3_4.csv", "x264-DB_4_5.csv", "x264-DB_5_6.csv",]

for file in files:
    print file
    data = pd.read_csv(file)
    columns = data.columns
    indep_columns = [c for c in data.columns if "<$" not in c]
    dep_columns = [c for c in data.columns if '<$' in c]
    pca = PCA(n_components=9)
    X_reduced = pca.fit_transform(data[indep_columns])
    X = pd.DataFrame(X_reduced)
    # print len(X.columns), len(data[dep_columns[0]]), len(data[dep_columns[1]]), len(data)
    X['<$1'] = data[dep_columns[0]]
    X['<$2'] = data[dep_columns[1]]
    # print len(X.columns), len(columns)
    column_names = ['$'+str(i+1) for i in xrange(9)]
    X.columns = column_names + ['<$1', '<$2']

    X.to_csv('reduced_'+file, index=False)




