====
# Chape_pred

## Overview
ChapePred is a program which based on a machine-learning algorithm (DNN) to predict protein solubilities under the three protein chaperones (TF, DnaKJE, and GroEL/ES).


## Description

## Requirement
・Python 3.x (3.7.8) 



## Usage
1. Install dependency packages
2. 
conda install --file requirements.txt

OR

Mannually install the python packages in the requirements.txt


2. Prepare FASTA formatted sequence

The file needs a single sequence and title line.
Line breaks in sequence is allowed.


3. Run Chapepred!

python chapepred.py input.fa


4. Result
PNG image contains solubility around each residue and
the average solubilities for three chaperones.
Text file contains predicted solubility without chaperone,with TF, KJE, and GroEL.

## Author
T. Yasuda, R. Morita, Y. Shigeta, R. Harada
