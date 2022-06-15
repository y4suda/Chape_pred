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
sol_model = load_model('lib/sol_model.h5')
sol_sc_Y = load(open("lib/sol_sc_Y.pkl", "rb"))
sol_sc_X = load(open("lib/sol_sc_X.pkl", "rb"))

#parmeter_setting
RESIDUE_NUMBER = 150
acid = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
plt.rcParams["font.size"] = 15

def convert_sequence(raw_sequence):
    if len(raw_sequence) != 0:
        aminoacid_proportion=[]
        for ac in acid:
            aminoacid_proportion.append(raw_sequence.count(ac)/len(raw_sequence))
    else:
        aminoacid_prpportion=[]
    return aminoacid_proportion

def predict_sol(job_id, raw_seq):
    
    #convert sequence
    sequence_length = len(raw_seq)
    max_window = sequence_length - 75
    converted_sequence = []
    for seq_num in range(len(raw_seq) - RESIDUE_NUMBER):
        converted_sequence.append(convert_sequence(raw_seq[seq_num:seq_num + RESIDUE_NUMBER]))
    converted_sequence_std = sol_sc_X.transform(converted_sequence)
    
    #prediction 
    result=(sol_model.predict(converted_sequence_std, verbose=0))
    result_inv=sol_sc_Y.inverse_transform(result)

    average_data = []
    std_data = []
    for i in range(1):
        average_data.append(np.average(result_inv[:,i]))
        std_data.append(np.std(result_inv[:,i]))
    return [ result_inv,average_data,std_data]

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
    
    #get control solubility
    control = predict_sol(job_id, raw_seq)

    #save data as text
    result_save = np.concatenate([control[0], result_inv], axis=1)
    np.savetxt(f"./result_data/{job_id}.txt", result_save)
     
    #draw graph
    fig = plt.figure(figsize=(13, 5))
    spec = gridspec.GridSpec(ncols=3, nrows=1,
                         width_ratios=[2, 1.2,0.4], wspace=0.3)
    c = ["deeppink", "dodgerblue", "limegreen"]
    l = ["TF", "KJE", "GroEL"]
    average_data = []
    std_data = []
    ax1 = fig.add_subplot(spec[0])
    for i in range(3):
        ax1.plot(result_inv[:,i], c=c[i], linewidth=2)
        average_data.append(np.average(result_inv[:,i]))
        std_data.append(np.std(result_inv[:,i]))
    ax1.plot(control[0], c="grey", linewidth=2)
    ax1.set_xlabel("Residue Number")
    ax1.set_ylabel("Solubility [%]")
    ax1.set_ylim(0, 130)
    ax1.set_xlim(0, sequence_length-150)
    ax1.set_xticks(np.linspace(0, sequence_length-150,10, dtype = 'int'))
    ax1.set_xticklabels(np.linspace(75, max_window,10, dtype = 'int') )
    
    ax2 = fig.add_subplot(spec[1])
    ax2.set_ylabel("Solubility [%]")
    ax2.set_ylim(0, 130)
    bar_list = ax2.bar(l, average_data, yerr=std_data, ecolor="black", capsize=10)
    for i in range(3):
        bar_list[i].set_color(c[i])
    ax2.axhline(control[1][0], color="red", linewidth=5, linestyle="dotted")
    ax3 = fig.add_subplot(spec[2])
    position=ax3.get_position()
    ax3.set_position([ax2.get_position().x0+ax2.get_position().width+0.01, position.y0, position.width, position.height])
    hist=np.loadtxt("./lib/sol_hist.txt")
    ax3.tick_params(labelbottom=False,
               labelleft=False,
               labelright=False,
               labeltop=False)
    ax3.barh([x for x in range(len(hist))], hist, color="lightgrey")
    plt.savefig(f"./result_data/{job_id}.png", dpi=300, bbox_inches="tight", pad_inches=0.01)
    return True
