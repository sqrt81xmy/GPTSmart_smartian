import os

baseDir = "/home/mingyue/Smartian/B3/output"

with open("./error2.txt") as file:
    content = file.readlines()
for line in content:
    line  = line.replace("_seed.txt\n","_normalFuncs.txt")
    seed_path = os.path.join(baseDir,line)
    if os.path.exists(seed_path):
        print(seed_path)
        os.remove(seed_path)
