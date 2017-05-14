from decimal import *
import time

tic = time.time()
getcontext().prec = 32
old = Decimal('3.14')
n = 4
S = Decimal('0.5')
pi = n * S.sqrt()
k = 1
while old!=pi:
  print("%3d %s" % (k, pi))
  old = pi
  n *= 2
  S = (1 - (1-S).sqrt()) / 2
  pi = n * S.sqrt()
  k+=1

toc= time.time()
print("time: %f seconds" % (toc-tic))
