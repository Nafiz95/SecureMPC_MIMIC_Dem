from mpyc.runtime import mpc

mpc.run(mpc.start())     # connect to all other parties
print(''.join(mpc.run(mpc.transfer('Hello world!'))))
mpc.run(mpc.shutdown())  # disconnect, but only once all other parties reached this point
