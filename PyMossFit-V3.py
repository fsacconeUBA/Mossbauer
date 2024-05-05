import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize, fit_report
from scipy.constants import *
from scipy.integrate import trapz

"""
Para doblar, normalizar y calibrar en mm/s, los archivos del espectrómetro de INTECIN de 1024 canales
"""
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

np.savetxt('19NOV14.csv', list(zip(x,y)), delimiter=",",fmt='%1.6e')

"""
LECTURA DE ARCHIVO DE ENTRADA
"""
col_list=[0, 1]

x, y= np.loadtxt("19NOV14.csv", delimiter=",", usecols=col_list, unpack=True)

"""
DEFINICIÓN DE LAS FUNCIONES DE AJUSTE (LORENTZIANAS)
"""

def singlet(a, b, m, x):
	return 2*a*b/(pi*(b**2+4*(x-m)**2))

def doublet(a, b, m, d, x):
	return 2*a*b/(pi*(b**2+4*(x-(m-d))**2))+2*a*b/(pi*(b**2+4*(x-(m+d))**2))

def sextet(a, b, m, d, q, l23, x):
	return 6*a*b/(pi*(b**2+4*(x-(m+5*d))**2))+l23*2*a*b/(pi*(b**2+4*(x-(m+3*d-q))**2))+2.5*a*b/(pi*(b**2+4*(x-(m+0.75*d))**2))+2.5*a*b/(pi*(b**2+4*(x-(m-0.75*d))**2))+l23*2*a*b/(pi*(b**2+4*(x-(m-3*d+q))**2))+6*a*b/(pi*(b**2+4*(x-(m-5*d))**2))

def linear_fitting_lmfit(params, x, y):
	b= params['b']; m= params['m']; d= params['d']; a= params['a']; q= params['q']; l23= params['l23']
		
	y_fit= 1-(sextet(a, b, m, d, q, l23, x))
	
	return y_fit-y
	
"""
AJUSTE DE LOS PARÁMETROS USANDO LOS DATOS EXPERIMENTALES
"""	
params= Parameters()

params.add('b', value= 0.3, vary=True)
params.add('m', value= -0.11, vary=True)
params.add('d', value= 1.07, vary=True)
params.add('a', value= 0.13, vary=True)
params.add('q', value= 0.0, vary=True)
params.add('l23', value= 2.0, vary=True)

fitted_params= minimize(linear_fitting_lmfit, params, args=(x, y,), method='least_square')

m= fitted_params.params['m'].value
b= fitted_params.params['b'].value
d= fitted_params.params['d'].value
a= fitted_params.params['a'].value
q= fitted_params.params['q'].value
l23= fitted_params.params['l23'].value


"""
CREACIÓN DE LOS SUBESPECTROS AJUSTADOS
"""
z1= 1-(sextet(a, b, m, d, q, l23, x))
e= y-z1
	
"""
INTEGRAL DE ÁREAS Y GENERACIÓN DE LOS PARÁMETROS HIPERFINOS. REPORTE EN PANTALLA
"""
i1= trapz(1-z1, x)

b= "{0:.2f}".format(b/np.sqrt(2))
m= "{0:.3f}".format(m)
h1= "{0:.1f}".format(5*d*33/5.312)
a= "{0:.4f}".format(a)
q= "{0:.2f}".format(q)
l23= "{0:.1f}".format(l23)
i1= "{0:.1f}".format(abs(i1))


print('ancho1 (sigma/sqrt(2)) es:', b, 'mm/s')
print('Centroide1 (ISO1) es:', m, 'mm/s')
print('Amplitud (a) es:', a)
print('B (Campo1) es:', h1, 'T')
#print('área:', i1, '%')
print(fit_report(fitted_params))

"""
GRAFICA DE ESPECTROS Y SUBESPECTROS
"""
plt.style.use('bmh')

fig, (ax1, ax2) = plt.subplots(2, sharex=True, height_ratios=[1,3.5]); fig.suptitle("CAL 19NOV14")
ax1.scatter (x, e, c= 'black')
ax1.set_ylim(-4,4)
ax1.set_ylabel('Error (%)')

ax2.scatter (x, y, c= 'black')
ax2.set_xlabel('V(mm/s)')
ax2.set_ylabel('Relative Transmission(a.u.)')
ax2.plot(x, z, c='red')

plt.show()

"""
GENERACIÓN DE ARCHIVOS DE SALIDA: DATOS Y PARÁMETROS
"""
np.savetxt('19NOV14-plot.csv', list(zip(x,y, z1)), fmt='%1.6e')

df= pd.DataFrame ({'Ancho(mm/s)': [b], 'ISO (mm/s)': [m], 'Quadrupolar shift': [q],'H/QUAD(T/mm-s)': [h1], 'Área(%)': [i1]})
df.to_csv('19NOV14_report.csv', index=False)
