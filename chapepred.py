import sys
import datetime
import numpy as np
import os 

print()
print("######################################")
print("##            Chapepred             ##")
print("######################################")
print("")
print("T. Yasuda, R. Morita, Y. Shigeta, R. Harada")
print("Center for Computational Sciences, University of Tsukuba")
print("")


print("")
print("Loading library and trained parameters.")
print("")

from lib import chape_pred_main


dir = './result_data'
if not os.path.exists(dir):
    os.makedirs(dir)

#job_id=str(datetime.datetime.now()).replace(" ", "-").replace(":", "-")
job_id = None
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith(">"):
            job_id = line.strip().replace(">", "").replace(" ", "_")

if job_id == None:
    print("Error: No title in FASTA file")
    exit(0)

print("Job ID is ", job_id)
print()

with open(sys.argv[1]) as f:
    sequence = "".join([line if not line.startswith(">") else "" for line in f])

print("Your input sequence is ...")
print(sequence)
print("")


result_message = chape_pred_main.predict_chape(job_id, sequence)
if result_message is not True:
    print("Error: something wrong...")
    sys.exit(1)
result=np.loadtxt(f"./result_data/{job_id}.txt")
average=np.average(result, axis=0)


print("")
print("          [    TF         KJE          GroE   ]")
print("Average: ", average)
print("")
print("")



