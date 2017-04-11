from sklearn.decomposition import PCA
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# files = [f for f in os.listdir('.') if ".csv" in f]
files = ["TriMesh_1_2.csv", "TriMesh_2_3.csv", "SaC1_2.csv", "SaC_11_12.csv", "SaC_3_4.csv", "SaC_5_6.csv", "SaC_7_8.csv", "SaC_9_10.csv", "x264-DB_1_2.csv", "x264-DB_2_3.csv", "x264-DB_3_4.csv", "x264-DB_4_5.csv", "x264-DB_5_6.csv",]

for file in files:
    data = pd.read_csv(file)
    indep_columns = [c for c in data.columns if "<$" not in c]
    pca = PCA(n_components=9)
    X_reduced = pca.fit_transform(data[indep_columns])
    np.savetxt('reduced_' + file, X_reduced, delimiter=',')




