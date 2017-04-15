import os

files = [f for f in os.listdir(".") if "al1-" in f]
files += [f for f in os.listdir(".") if "al2-" in f]
files += [f for f in os.listdir(".") if "mmre-" in f]
files += [f for f in os.listdir(".") if "rank-" in f]

import pdb
pdb.set_trace()

for file in files:
    cmd = "python " + file + "&"
    os.system(cmd)