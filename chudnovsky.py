from decimal import *
import time

tic = time.time()
getcontext().prec = 128
old = Decimal('3.14')
K = Decimal(6)
M = X = Decimal(1)
L = S = Decimal(13591409)
A = Decimal(10005).sqrt()
pi = 426880 * A / S
k = 1
while old!=pi:
  print("%3d %s" % (k, pi))
  old = pi
  M = (K**3 - K*16) * M / Decimal(k)**3 
  L += Decimal(545140134)
  X *= Decimal(-262537412640768000)
  S += M * L / X
  K += 12
  pi = 426880 * A / S
  k+=1

toc= time.time()
print("time: %f seconds" % (toc-tic))
