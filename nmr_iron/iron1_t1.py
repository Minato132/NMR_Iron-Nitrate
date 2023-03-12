import numpy as np
import scipy.optimize as py
import matplotlib.pyplot as plt
import pandas as pd


def T1(t, a, b, c, d):
	return 1 - np.exp(-1/b * t + c) + d


def p(ar1, ar2, func, err):
	a, b = py.curve_fit(func, ar1, ar2, sigma = err, method = 'trf')
	return a, b 


#_____________________________________________________________________________


with open('/home/minato132/Documents/Data/Iron1/iron1_t1.csv') as file:
	data = pd.read_csv(file)

data.rename(columns = {'Delay time ms': 'dtime', 'Max Voltage (V)' : 'amp'}, inplace = True)

data.loc[:10, 'amp'] = data.loc[:10, 'amp'] * - 1

error = []
for i in data['amp']:
	if i < 0:
		i *= -.01
		error.append(i)
	else:
		i *= .01
		error.append(i)

error = pd.Series(error, name = 'Error')

data = data.merge(error, left_index = True, right_index = True)


def t1(ar1, ar2, ar3):
	a, b = p(ar1, ar2, T1, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'blue', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T1(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Delay Time (ms)')
	plt.ylabel('Maximum Amplitude (V)')
	plt.title('T1 of Iron Nitrate (%1.01)')
	plt.legend()

	print(*a, f'\n Error for b is {b[2,2]}')
	plt.show()

	return 0


print(t1(data['dtime'], data['amp'], data['Error']))



