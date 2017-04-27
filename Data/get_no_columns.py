import os
import pandas as pd

files = [f for f in os.listdir('.') if ".csv" in f]
columns_dict = {}
for file in files:
    content = pd.read_csv(file)
    columns = content.columns
    decisions = [c for c in columns if '<$' not in c]
    columns_dict[file[:-4]] = len(decisions)

import pdb
pdb.set_trace()

