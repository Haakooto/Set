import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time


id = input()
fil = "data.txt"
null_msg = "game not started"
end = False

while True:

    with open(fil, "r") as file:
        lines = file.readlines()

    if lines[0] == null_msg:
        if end:
            break
        else:
            end = True
        with open(fil, "w")as file:
            file.write(f"adding line from {id}\n")

    else:
        with open(fil, "a") as file:
            file.write(f"appending line from {id}\n")

    with open(fil, "r") as file:
        print(file.read())

    time.sleep(3)

    # if input() == "end":
        # break

with open(fil, "w") as file:
    file.write(null_msg)