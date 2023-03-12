import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as py
import pandas as pd


def T2p(t, a, b, c, d):
	y = np.exp(-1/b * t + c) + d
	return y

def p(ar1, ar2, func, err):
	a, b = py.curve_fit(func, ar1, ar2, sigma = err, method = 'trf')
	return a, b 


with open('/home/minato132/Documents/Data/Iron1/iron1_t2p.csv') as file:
	data = pd.read_csv(file)
	data['CH1'] = pd.to_numeric(data.loc[1:, 'CH1'])

time = []
x = data.iat[0, 2]
i = 0
while i < len(data['X']) - 1:
	time.append(x)
	x += data.iat[0, 3]
	i += 1 

time = pd.Series(time, index = np.arange(1, 1201))

err = []
for i in data['CH1']:
	i *= .01
	err.append(i)

d = {'time' : time, 'amp' : data['CH1'], 'err' : err}

data = pd.DataFrame(d)
data.drop(0, axis = 0, inplace = True)
data = data.loc[data['amp'] > 0]

def t2p(ar1, ar2, ar3):
	a, b = p(ar1, ar2, T2p, ar3)
	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'blue', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T2p(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Time (ms)')
	plt.ylabel('Voltage (V)')
	plt.title("T2' of 1.01% Iron Nitrate")
	plt.legend()

	print(*a, f'\n Error of b is {b[1,1]}')
	plt.show()
	return 0

data = data.loc[data['time'] > 0]
data = data.loc[data['time'] < .0043]
data['time'] = data['time'] * 1000 
pd.set_option('display.max_rows', None)

data = data.loc[[444, 541, 641], :]

print(t2p(data['time'], data['amp'], data['err']))

