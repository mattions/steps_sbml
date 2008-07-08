## Setting the directory
import os
free = False
index = 0
dir = "Sims/Sim_%d" %index

while not free :
    if os.path.exists(dir):
        index = index + 1
        dir = "Sims/Sim_%d" %index
    else:
        free = True
        os.mkdir(dir)
