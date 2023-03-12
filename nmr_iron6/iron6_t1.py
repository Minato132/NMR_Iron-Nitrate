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


with open('/home/minato132/Documents/Data/iron6/iron6_t1.csv') as file:
	data = pd.read_csv(file)
	data.rename(columns = {'Delay Time' : 'time', 'Max Voltage (': 'amp'}, inplace = True)

data.loc[:20, 'amp'] = data.loc[:20, 'amp'] * -1

err = []
for i in data['amp']:
	if i < 0:
		i *= -.01
		err.append(i)
	else:
		i *= .01
		err.append(i)

err = pd.Series(err, name = 'Error')
data = data.merge(err, left_index = True, right_index = True)

def t1(ar1, ar2, ar3):
	a, b = p(ar1, ar2, T1, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'blue', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T1(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Delay Time (ms)')
	plt.ylabel('Max Amplitude')
	plt.title('T1 for .6% Iron Nitrate')
	plt.legend()

	print(*a, f'\n Error of b is {b[1,1]}')
	plt.show()


print(t1(data['time'], data['amp'], data['Error']))
