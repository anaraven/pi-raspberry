---
layout: "post"
title: "Calculando Pi en Raspberry Pi"
date: "2017-04-30 11:25"
lang: es
---

La relación entre el radio de  un círculo y su perímetro ha intrigado a la gente desde la antigüedad. Un problema clásico que muchos trataron de resolver es la "cuadratura del círculo": cómo dibujar, usando sólo regla y compás, un cuadrado con la misma área que un círculo de radio 1. El problema no puede ser resuelto pues el círculo tiene un area de tamaño $\pi$, que es un número *trascendente*, es decir, que no puede obtenerse con regla y compás.

El valor exacto de $\pi$ es difícil de calcular. Muchos matemáticos han inventado fórmulas para calcularlo, y cada nuevo modelo de super-computador ha roto el récord del número de dígitos de $\pi$ calculados.

No obstante el modesto tamaño del Raspberry Pi, éste posee todas las herramientas necesarias para calcular varios miles de dígitos de $\pi$.


# Idea de Arquímedes
El sabio Arquímedes vivió en XX. Entre los muchos problemas que resolvió, Arquímedes se dio cuenta que un polígono regular con muchos lados (digamos $n$) se parece cada vez más a un círculo. Y es fácil calcular el perímetro de un polígono. Si dibujamos el polígono dentro de un círculo de radio 1, de modo que los ángulos del polígono estén en el círculo, cada lado cubrirá un ángulo de $360^o/n$. Por ejemplo un octógono tiene 8 lados iguales. Cada lado cubre $360/8$ grados, es decir, 45 grados.

Un poco de trigonometría nos muestra que el largo de cada uno de los lados es $2\sin(360^o/2n)$. Es decir el perímetro del polígono de $n$ lados inscrito en el círculo es
$$2n\sin\left(\frac{360^o}{2n}\right).$$

¿Cómo podemos calcular el valor de esa función trigonométrica? Podemos usar varias propiedades que son conocidas desde tiempos antiguos. Sabemos que, para cualquier ángulo $\theta$ siempre se cumple que
$$\sin^2(\theta)+\cos^2(\theta)=1$$
y que
$$\cos(\theta)=\cos^2(\theta/2)-\sin^2(\theta/2).$$
Combinando ambas fórmulas podemos deducir que
$$\sin^2(\theta/2)=\frac{1-\sqrt{1-\sin^2(\theta)}}{2}$$
que nos permite calcular $\sin(\theta/n)$ para $n=2^k$ tan grande como queramos.

```python
from decimal import *

getcontext().prec = 30
S = Decimal('0.5')
n = 4
for i in range(30):
  S = (1 - (1-S).sqrt()) / 2
  n = n * 2
  print(n * S.sqrt())
```

# Arco tangente
Como $\tan(\pi/4)=1$ se deduce que
$$\pi = 4\cdot\arctan(1)$$

# Fórmula de Machin
$$\pi = 16·\arctan(1/5) − 4·\arctan(1/239)$$

# Los hermanos Chudnovsky

```python
from decimal import *

getcontext().prec = 50
K = Decimal(6)
M = X = Decimal(1)
L = S = Decimal(13591409)
A = Decimal(10005).sqrt()
for k in range(1, 10):
  M = (K**3 - K*16) * M / Decimal(k)**3 
  L += Decimal(545140134)
  X *= Decimal(-262537412640768000)
  S += M * L / X
  K += 12
  pi = 426880 * A / S
  print(pi)
```

```python
from decimal import *

getcontext().prec = 10000
K = Decimal(6)
M = X = Decimal(1)
L = S = Decimal(13591409)
for k in range(1, 301):
  M = (K**3 - K*16) * M / Decimal(k)**3 
  L += Decimal(545140134)
  X *= Decimal(-262537412640768000)
  S += M * L / X
  K += 12

pi = 426880 * Decimal(10005).sqrt() / S
print(pi)
```

----

### Idea para una charla
Digamos, para el 14 de marzo o el 28 de junio (tau day). O un poster "Pi en Raspberry pi"

Como Python maneja enteros de precisión infinita, se puede usar una representación

¿cómo calcular Pi?

+ Taylor expansion
+ calculando E : `2016/sysbio/_src/Exponential.ipynb`
+ Seguir la monografía de análisis numérico por Axel Osses: `~/Documents/MonografiaAN.pdf`
+ Archimedes: $n \sin(360/n)$
+ elegir el buen $n$ usando la identidad trigonométrica 
    + $\cos(2\theta)=\cos^2(\theta)-\sin^2(\theta)$
    + $\sqrt{1-\sin^2(2\theta)}=1-2\sin^2(\theta)$
    + $\sin(\theta/2)=\frac{1-\sqrt{1-\sin^2(\theta)}}{2}$
+ i.e. para $x_i=\sin^2(360/2^i)$ tenemos
    + $x_2=\sin^2(90)=1$
    + $x_{i+1}=\frac{1-\sqrt{1-x_i}}{2}$
    + $2^i\sqrt{x_i}\rightarrow\pi$

+ ¿cómo calcular raíces cuadradas?
    + El número de dígitos de la representación en punto fijo debe ser par. Es decir $x$ se representar por $x\cdot 10^{2N}$, de modo que $\sqrt{x\cdot 10^{2N}}$ se representa por $\sqrt{x}\cdot 10^{N}$ 
    + https://github.com/aleaxit/gmpy and https://pypi.python.org/pypi/gmpy2
    + https://programmingpraxis.com/2012/06/01/square-roots/
    ```python
    def isqrt(n):
      x = n
      y = (x + 1) // 2
      while y < x:
        x = y
        y = (x + n // x) // 2
      return x
    ```
    + Alternativamente, usar `decimal` en Python
+ Euler? raíces de $\sin(\sqrt x)/\sqrt{x}$ son $\pi^2$. Luego
$$1+1/2^2+1/3^2 +\cdots = \pi^2/6$$
```python
six = 6*10**20
acc=0
for i in range(5000000000):
    term = six//(i+1)
    acc += term//(i+1)
    if i % 10000000==0:
      print(acc," ",i)
```
+ calculando $4 \arctan(1)$
```python
four=4*10**50
acc=0
sgn=1
for i in range(5000000000):
    term = four//(2*i+1)
    acc += term*sgn
    sgn = -sgn
    if i % 10000000==0:
      print(acc," ",i)
```
+ convergencia: muy lenta
+ Machin idea: http://turner.faculty.swau.edu/mathematics/materialslibrary/pi/machin.html
+ http://www.pi314.net/eng/machin.php
+ 16·arctan(1/5) − 4·arctan(1/239)
+ paralelizar, al menos en 3 partes
    + $(-1/5)^{2i+1}$
    + $(-1/239)^{2i+1}$
    + $1/(2i+1)^i$
    + algo que junte todo
+ ver si se puede hacer en iPython/jupyter
    + en el servidor
    + en un raspberry
    + en un cluster de raspberry

+ Biblioteca `decimal` en python: precisión arbitraria
+ el mejor: 14 decimales por iteración
```python
from decimal import Decimal as Dec, getcontext as gc

def PI(maxK=70, prec=1008, disp=1007): # parameter defaults chosen to gain 1000+ digits within a few seconds
    gc().prec = prec
    K = Dec(6)
    M = X = Dec(1)
    L = S = Dec(13591409)
    for k in range(1, maxK+1):
        M = (K**3 - K*16) * M / Dec(k)**3 
        L += Dec(545140134)
        X *= Dec(-262537412640768000)
        S += M * L / X
        K += 12
    pi = 426880 * Dec(10005).sqrt() / S
    pi = Dec(str(pi)[:disp]) # drop few digits of precision for accuracy
    print("PI(maxK=%d iterations, gc().prec=%d, disp=%d digits) =\n%s" % (maxK, prec, disp, pi))
    return pi

Pi = PI()
```
+ https://math.stackexchange.com/questions/180274/what-would-the-chudnovsky-algorithm-look-like-as-an-inifinite-series
+ http://numbers.computation.free.fr/Constants/constants.html
+ quizá se puede paralelizar, calculando M, L y X por separado
    + main process crea 3 pipes de lectura, lanza Mfactory, Lfactory y Xfactory y colecta M, L, X para actualizar S
    + pueden ser threads
