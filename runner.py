import os

files = [f for f in os.listdir(".") if "al1" in f]
files += [f for f in os.listdir(".") if "al2" in f]

for file in files:
    cmd = "python " + file + "&"
    os.system(cmd)