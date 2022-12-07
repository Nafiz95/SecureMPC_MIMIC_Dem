# SecureMPC_MIMIC_Dem
Toy experiments on MIMIC III Demo dataset using SMC


This a toy experiment for CISC870 (Cryptography) at Queen's University, Kingston, ON, Canada. The experiment is conducted on the MIMIC III Dataset (please cite https://physionet.org/content/mimiciii-demo/1.4/).

Two tables are used:
1. Patients.csv
2. Prescriptions.csv

The experiment uses MPyC library (https://www.win.tue.nl/~berry/mpyc/) to do two tasks:
- Securely add prescribed doses.
- Securely permute patients.

Prerequistes:
1. pip install pandas
2. pip install mpyc

To run experiment:
python3 file.py -M2 (for 2 party)
python3 file.py -M3 (for 3 party)
