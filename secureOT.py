import pandas as pd
import time
from mpyc.runtime import mpc    # load MPyC
#secint = mpc.SecInt()           # 32-bit secure MPyC integers
#mpc.run(mpc.start())            # required only when run with multiple parties
#import traceback      

import random
import sys


#patient = pd.read_csv('PATIENTS.csv')

#prescription = pd.read_csv('PRESCRIPTIONS.csv')
patient_id = 12 #[1,2,3] #patient.subject_id
pres_id = 14 #[4,5,6,7]  #prescription.hadm_id.unique().tolist()

m = len(mpc.parties)
if m%2 == 0:
    print('OT runs with odd number of parties only.')
    sys.exit()
    
    
t = m//2
message = [(None, None)] * t
choice = [None] * t

mpc.pid=1

if mpc.pid == 0:
    print('You are the trusted third party.')
elif 1 <= mpc.pid <= t:
    print(mpc.pid)
    message[mpc.pid - 1] = (patient_id, pres_id)
    print(f'You are sender {mpc.pid} holding messages '
          f'{message[mpc.pid - 1][0]} and {message[mpc.pid - 1][1]}.')
else:
    choice[mpc.pid - t - 1] = 0 # 0->patient id, 1->pres id
    print(f'You are receiver {mpc.pid - t} with random choice bit {choice[mpc.pid - t - 1]}.')
    
mpc.run(mpc.start())

secnum = mpc.SecInt()
for i in range(1, t+1):
    x = mpc.input([secnum(message[i-1][0]), secnum(message[i-1][1])], i)
    b = mpc.input(secnum(choice[i-1]), t + i)
    a = mpc.run(mpc.output(mpc.if_else(b, x[1], x[0]), t + i))
    if a is not None:
        print(f'You have received message {a}.')
mpc.run(mpc.shutdown())   # required only when run with multiple parties
