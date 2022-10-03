import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize, fit_report
from scipy.constants import *
from scipy.integrate import trapz

col_list=[0, 1]

x, y= np.loadtxt("19NOV14.csv",delimiter=" ", usecols=col_list, unpack=True)

def linear_fitting_lmfit(params, x, y):
	b1= params['b1']; m1= params['m1']; d1= params['d1']; a1= params['a1']; q1= params['q1']
		
	y_fit= (1-a1*b1/(pi*(b1**2+(x-(m1-d1+q1)/2)**2))-a1*b1/(pi*(b1**2+(x-(m1+d1-q1)/2)**2))
	-2*a1*b1/(pi*(b1**2+(x-(m1-3*d1+q1)/2)**2))-2*a1*b1/(pi*(b1**2+(x-(m1+3*d1-q1)/2)**2))
	-3*a1*b1/(pi*(b1**2+(x-(m1-5*d1)/2)**2))-3*a1*b1/(pi*(b1**2+(x-(m1+5*d1)/2)**2)))
		
	return y_fit-y
	
params= Parameters()

params.add('b1', value= 0.25, vary=True)
params.add('m1', value= -0.11, vary=True)
params.add('d1', value= 1.5, vary=True)
params.add('a1', value= 0.05, vary=True)
params.add('q1', value= 0.01, vary=True)

fitted_params= minimize(linear_fitting_lmfit, params, args=(x, y,), method='least_square')

m1= fitted_params.params['m1'].value
b1= fitted_params.params['b1'].value
d1= fitted_params.params['d1'].value
a1= fitted_params.params['a1'].value
q1= fitted_params.params['q1'].value

z1= (1-a1*b1/(pi*(b1**2+(x-(m1-d1+q1)/2)**2))-a1*b1/(pi*(b1**2+(x-(m1+d1-q1)/2)**2))
	-2*a1*b1/(pi*(b1**2+(x-(m1-3*d1+q1)/2)**2))-2*a1*b1/(pi*(b1**2+(x-(m1+3*d1-q1)/2)**2))
	-3*a1*b1/(pi*(b1**2+(x-(m1-5*d1)/2)**2))-3*a1*b1/(pi*(b1**2+(x-(m1+5*d1)/2)**2)))
	
	

i = trapz(1-z1, x)

b1= "{0:.2f}".format(b1)
m1= "{0:.3f}".format(m1)
h1= "{0:.1f}".format(5*d1*33/2/5.312)
a1= "{0:.2f}".format(a1)
e1= "{0:.2f}".format(q1/2)
i1= "{0:.1f}".format(i)

plt.style.use('bmh')

plt.scatter (x, y, c= 'black')
plt.xlabel('V(mm/s)')
plt.ylabel('Relative Transmission(a.u.)')
plt.plot(x, z1, c='red')

plt.show()

print('ancho1 (sigma1) es:', b1, 'mm/s')
print('Centroide1 (ISO1) es:', m1, 'mm/s')
print('quadrupolar shift es:', e1, 'mm/s')
print('Amplitud1 (a1) es:', a1)
print('B1 (Campo1) es:', h1, 'T')

df= pd.DataFrame ({'Ancho(mm/s)': [b1], 'ISO (mm/s)': [m1], 'Quad Shift (mm/s)':[e1], 'H/QUAD(T/mm-s)': [h1]})
df.to_csv('19NOV14_report.csv', index=False)


