import pandas as pd
import time

patient = pd.read_csv('PATIENTS.csv')
patient_list = patient.index.tolist()[3:]

from mpyc.runtime import mpc    # load MPyC
secint = mpc.SecInt()           # 32-bit secure MPyC integers
mpc.run(mpc.start())            # required only when run with multiple parties
import traceback                # to show some suppressed error messages


@mpc.coroutine                                      # turn coroutine into an MPyC coroutine
async def random_unit_vector(n):                    # returns list of n secint elements
    await mpc.returnType(secint, n)                 # set return type of this MPyC coroutine
    if n == 1: 
        return [secint(1)]
    b = mpc.random_bit(secint)                      # pick one random bit if n>=2
    x = random_unit_vector((n + 1) // 2)            # recursive call with m=(n+1)//2
    if n % 2 == 0:
        y = mpc.scalar_mul(b, x)                    # y = [0]*m or y = x
        return y + mpc.vector_sub(x, y)             # [0]*m + x or x + [0]*m
    elif await mpc.eq_public(b * x[0], 1):          # reject if b=1 and x[0]=1
        return random_unit_vector(n)                # start over
    else:
        y = mpc.scalar_mul(b, x[1:])                # y = [0]*m or y = x[1:] 
        return x[:1] + y + mpc.vector_sub(x[1:], y) # [x[0]]  + ([0]*m + x[1:] or [0]*m + x[1:])

def random_permutation(n):                     # returns list of n secint elements
    p = [secint(i) for i in range(n)]          # initialize p to identity permutation
    for i in range(n-1):
        x_r = random_unit_vector(n-i)          # x_r = [0]*(r-i) + [1] + [0]*(n-1-r), i <= r < n
        p_r = mpc.in_prod(p[i:], x_r)          # p_r = p[r]
        d_r = mpc.scalar_mul(p[i] - p_r, x_r)  # d_r = [0]*(r-i) + [p[i] - p[r]] + [0]*(n-1-r)
        p[i] = p_r                             # p[i] = p[r]
        for j in range(n-i):
            p[i+j] += d_r[j]                   # p[r] = p[r} + p[i] - p[r] = p[i]
    return p                                

@mpc.coroutine                                    # turn coroutine into an MPyC coroutine
async def random_derangement(n):                  # returns list of n secint elements
    await mpc.returnType(secint, n)               # set return type of this MPyC coroutine
    p = random_permutation(n)
    t = mpc.prod([p[i] - i for i in range(n)])    # securely multiply all differences p[i] - i
    if await mpc.is_zero_public(t):               # publicly test whether t is equal to zero
        return random_derangement(n)              # recurse if t is zero
    else:
        return p                                  # done if t is nonzero
        
        
print('Random derangements:')
for n in patient_list:
    s = mpc.run(mpc.output(random_derangement(n)))
    print(f'{n:2} {s}')
    
    
mpc.run(mpc.shutdown())   # required only when run with multiple parties
