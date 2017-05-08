import os

folder = [f for f in os.listdir(".") if ".py" not in f]

print folder