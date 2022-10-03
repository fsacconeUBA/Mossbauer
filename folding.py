"""
Para doblar, normalizar y calibrar en mm/s, los archivos del espectrómetro de INTECIN de 1024 canales
"""

import numpy as np
import matplotlib.pyplot as plt

fecha = float(input('Ingrese la fecha de calibración (AAAAMMDD): '))
vel = float(input('Ingrese el rango de V (en mm/s): ' ))
np.savetxt('calib.txt', (fecha,vel), fmt='%f')

y= np.loadtxt('19NOV14.mos')

plt.plot(y)
plt.show()

for i in range(0, 511):
	y[[i]]=y[[i]]+y[[1023-i]]

y=y[0:511]

"""
Normalización
"""
y2=[y[0:59],y[451:510]]

ymax=np.mean(y2)
ymax=int(ymax)

print(ymax)

for i in range(0, 511):
	y[[i]]=y[[i]]/ymax


x=np.arange(1,512)

"""
de canales a escala de velocidades en mm/s
"""
v=np.loadtxt('calib.txt'); vmax=v[[1]]

x=np.linspace(start = 0, stop = 511, num= 512)

for i in range(0, 511):
	x[[i]]=-(i-256)*vmax/256

x=x[0:511]

plt.plot(x,y)	
plt.show()

np.savetxt('19NOV14.csv', list(zip(x,y)), fmt='%1.6e')
