import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-dark-palette')

col_list=[1, 2]
df = pd.read_csv (r'ESP3505-plot.dat')

ax= df.plot(kind= 'scatter', x=1, y=2, c= 'black', label= 'data')
df.plot(x = 1, y = [3, 4, 7, 8],label=[ 'Total', 'Fe1', 'Fe2','Fe3',], color= ['brown', 'g', 'g', 'g'], ls='-',ax=ax)
df.plot(x = 1, y = [ 5, 6, 9],label=[  'Fe bcc', 'FeB', 'Fe2B'], color= [ 'blue', 'violet', 'gray'], ls='--', ax=ax)
ax.set_xlabel('v(mm/s)',fontsize=12)
ax.set_ylabel('Relative Transmission (a. u.)',fontsize=12)
plt.grid()
plt.title("TT 685 - RT")
plt.show()
