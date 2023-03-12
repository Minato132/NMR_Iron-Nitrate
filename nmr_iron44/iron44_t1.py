import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as py

def T1(t, a, b, c, d):
	y = 1 - np.exp(-1/b * t + c) + d
	return y


def p(ar1, ar2, func, err):
	a, b = py.curve_fit(func, ar1, ar2, sigma = err, method = 'trf')
	return a, b

with open('/home/minato132/Documents/Data/iron44/iron44_t1.csv') as file:
	data = pd.read_csv(file)
	data.rename(columns = {'Delay Time (ms)' : 'time', 'Max Amp (V)' : 'amp'}, inplace = True)

data.loc[:4, 'amp'] = data.loc[:4, 'amp'] * -1

error = []
for i in data['amp']:
	if i < 0:
		i *= -.01
	else:
		i *= .01
	error.append(i)

def t1(ar1, ar2, ar3):
	a, b = p(ar1, ar2, T1, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T1(ar1, *a), label = 'Fitted Function')
	plt.xlabel('Delay Time (ms)')
	plt.ylabel('Maximum Amplitude (V)')
	plt.title('T1 of .44% Iron Nitrate')
	plt.legend()

	print(*a, f'\n Error of b is {np.sqrt(b[1,1])}')
	plt.show()
	return 0



print(t1(data['time'], data['amp'], error))
