import sys
import datetime
import numpy as np
from lib import chape_pred_main
import os 

print()
print("######################################")
print("##            Chapepred             ##")
print("######################################")
print("")
print("T. Yasuda, R. Morita, Y. Shigeta, R. Harada")
print("")

dir = './result_data'
if not os.path.exists(dir):
    os.makedirs(dir)

job_id=str(datetime.datetime.now()).replace(" ", "-").replace(":", "-")
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


print("          [ w/o chap.      TF         KJE          GroE   ]")
print("Average: ", average)
print("")
print("")



