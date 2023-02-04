#import modules
import os
import warnings
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from pickle import load
from matplotlib import gridspec

os.environ['TF_CPP_MIN_LOG_LEVEL']="2"
warnings.simplefilter('ignore')



#load model
model = load_model('lib/model.h5')
sc_Y = load(open("lib/sc_Y.pkl", "rb"))
sc_X = load(open("lib/sc_X.pkl", "rb"))

#parmeter_setting
RESIDUE_NUMBER = 150
acid = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
plt.rcParams["font.size"] = 9


def convert_sequence(raw_sequence):
    if len(raw_sequence) != 0:
        aminoacid_proportion=[]
        for ac in acid:
            aminoacid_proportion.append(raw_sequence.count(ac)/len(raw_sequence))
    else:
        aminoacid_prpportion=[]
    return aminoacid_proportion

def predict_chape(job_id,raw_seq):
    
    #convert sequence
    sequence_length = len(raw_seq)
    if sequence_length <= 150:
        return "Query sequence is too short (<150)."
    max_window = sequence_length - 75
    converted_sequence = []
    for seq_num in range(len(raw_seq) - RESIDUE_NUMBER):
        converted_sequence.append(convert_sequence(raw_seq[seq_num:seq_num + RESIDUE_NUMBER]))
    
    converted_sequence_std = sc_X.transform(converted_sequence)
    
    #prediction 
    result = (model.predict(converted_sequence_std))
    result_inv = sc_Y.inverse_transform(result)

    #save data as text
    np.savetxt(f"./result_data/{job_id}.txt", result_inv)
     
    #draw graph
    fig = plt.figure(figsize=((83/12.7)/3*2,1.6))
    spec = gridspec.GridSpec(ncols=2, nrows=1,
                         width_ratios=[1.0, 0.4], wspace=0.4)
    c = ["deeppink", "dodgerblue", "limegreen"]
    l = ["TF", "KJE", "GroEL"]

    average_data = []
    std_data = []
    ax1 = fig.add_subplot(spec[0])
    for i in range(3):
        ax1.plot(result_inv[:,i], c=c[i], linewidth=1.0)
        average_data.append(np.average(result_inv[:,i]))
        std_data.append(np.std(result_inv[:,i]))
    ax1.set_xlabel("Residue Number")
    ax1.set_ylabel("Solubility [%]")
    ax1.set_ylim(0, 130)
    ax1.set_xlim(0, sequence_length-150)
    ax1.set_xticks(np.linspace(0, sequence_length-150,10, dtype = 'int'))
    ax1.set_xticklabels(np.linspace(75, max_window,10, dtype = 'int'),Rotation=-40 )
    
    ax2 = fig.add_subplot(spec[1])
    ax2.set_ylabel("Solubility [%]")
    ax2.set_ylim(0, 130)
    bar_list = ax2.bar(l, average_data, yerr=std_data, ecolor="black", capsize=3)
    for i in range(3):
        bar_list[i].set_color(c[i])
    ax2.set_xticklabels(l,Rotation=-40 )
    
    plt.tight_layout()
    plt.savefig(f"./result_data/{job_id}.png", dpi=300, bbox_inches="tight", pad_inches=0.01)
    return True
