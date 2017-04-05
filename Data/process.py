from __future__ import division

import pandas as pd
import os

files = [ 'rs-6d-c3.csv', 
'sol-6d-c2.csv', 'wc+rs-3d-c4.csv', 'wc+sol-3d-c4.csv', 
'wc+wc-3d-c4.csv', 'wc-3d-c4.csv', 'wc-5d-c5.csv', 'wc-6d-c1.csv', 'wc-c1-3d-c1.csv', 'wc-c3-3d-c1.csv']

org_filename = "llvm.dat"
for f in files:
	data_filename = f.split('.')[0]
	filename = "./conf/" + data_filename + ".dat"
	lines = open(org_filename).readlines()
	data = pd.read_csv(f)
	columns = data.columns
	dependent = [c for c in columns if '<$' in c]
	independent = [c for c in columns if '<$' not in c]

	lines[0] = "name = " + data_filename + "\n"
	lines[1] = "num_features = " + str(len(independent)) + "\n"
	lines[2] = "readfile = train_data/" + data_filename + ".csv\n"
	lines[3] = "results_folder = results_" + data_filename + "/\n"

	assert(len(dependent) == 2), "Something is wrong"
	lines[6] = "train_data_range_obj1 = " + str(data[dependent[0]].max() - data[dependent[0]].min()) + "\n"
	lines[7] = "train_data_range_obj2 = " + str(data[dependent[1]].max() - data[dependent[1]].min()) + "\n"
	lines[13] = "number_of_repetitions = 40\n"
	
	lines[15] = "maximize_obj1 = 1\n"
	lines[16] = "maximize_obj2 = 0\n"

	thefile = open(filename, 'w')

	for item in lines:
	  thefile.write("%s" % item)
	thefile.close()
	os.system('mkdir results_' + data_filename + '/')
	os.system('touch results_' + data_filename + "/.keep")
	print filename, " is done "
