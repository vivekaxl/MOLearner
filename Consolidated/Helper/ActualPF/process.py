# consolidate the .p files

import pickle
import os

# files = [ f for f in os.listdir(".") if ".py" not in f ]
# for file in files:
#     content = pickle.load(open(file, 'r'))
#     print file, len(content.keys())


consolidated_dict = {}
files = ["actual_pf_SaC_9_10.p", "actual_pf_xomoo2-p10000-d27-o4-dataset3.p"]
for i, file in enumerate(files):
    print file
    content = pickle.load(open(file, 'r'))
    for key in sorted(content.keys()):
        consolidated_dict[key] = content[key]
        print key, len(consolidated_dict.keys())
all_files = [f for f in os.listdir(".") if ".py" not in f and "consolidated" not in f]
for i, f in enumerate(all_files):
    print i, f
assert(len(all_files) == len(consolidated_dict.keys())), "Something is wrong"
pickle.dump(consolidated_dict, open("consolidated_dict.p", 'w'))