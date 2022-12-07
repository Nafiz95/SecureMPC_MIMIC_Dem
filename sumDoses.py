
import pandas as pd
import time


#data

prescription = pd.read_csv('PRESCRIPTIONS.csv')
dose_val_rx=prescription.dose_val_rx.tolist()
doses = []
for i in prescription.dose_val_rx.tolist():
    try:
        if eval(i)>0:
            doses.append(int(eval(i)))
    except:
        pass


from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties

#Checking with normal summation
start_time = time.time()

total_dose = sum(doses)
print("--- %s seconds ---" % (time.time() - start_time))

#Checking with secure summation
start_time = time.time()
x = list(map(secint, doses))
summation = secint(0)
for i in x:
    summation+=i
print("--- %s seconds ---" % (time.time() - start_time))

mpc.run(mpc.shutdown())   # required only when run with multiple parties
