from decimal import *
import time

def archimedes(prec):
  getcontext().prec = prec
  old = Decimal('3.14')
  n = 4
  S = Decimal('0.5')
  pi = n * S.sqrt()
  k = 1
  while old!=pi:
    old = pi
    n *= 2
    S = (1 - (1-S).sqrt()) / 2
    pi = n * S.sqrt()
    k+=1
  return pi

def chudnovski(prec):
  getcontext().prec = prec
  old = Decimal('3.14')
  K = Decimal(6)
  M = X = Decimal(1)
  L = S = Decimal(13591409)
  A = 426880 * Decimal(10005).sqrt()
  pi = A / S
  k = 1
  while old!=pi:
    old = pi
    M = (K**3 - K*16) * M / Decimal(k)**3
    L += Decimal(545140134)
    X *= Decimal(-262537412640768000)
    S += M * L / X
    K += 12
    pi = A / S
    k+=1
  return pi

def timeit(fun, param):
  tic = time.time()
  fun(param)
  toc= time.time()
  return (toc-tic)

if __name__ == '__main__':
  n=32
  for i in range(9):
    print("%d\t%f" % (n, timeit(chudnovski, n)))
    # print("%d\t%f\t%f" % (n, timeit(archimedes, n), timeit(chudnovski, n)))
    n *= 2
