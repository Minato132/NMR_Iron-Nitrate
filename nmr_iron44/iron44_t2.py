import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as py

def T2(t, a, b, c, d):
	y = np.exp(-1/b * t + c) + d
	return y


def p(ar1, ar2, func):
	a, b = py.curve_fit(func, ar1, ar2, method = 'trf')
	return a, b


with open('/home/minato132/Documents/Data/iron44/iron44_t2.csv') as file:
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

error = []
for i in data['CH1']:
	i *= .01
	error.append(i)

d = {'time' : time, 'amp' : data['CH1'], 'err' : error}

data = pd.DataFrame(d)
data.drop(0, axis = 0, inplace = True)

def t2(ar1, ar2, ar3): 
	a, b = p(ar1, ar2, T2)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T2(ar1, *a), label = 'Fitted Curve')
	plt.xlabel('Time')
	plt.ylabel('Voltage')
	plt.title('T2 of .44% Iron Nitrate')
	plt.legend()

	print(*a, f'\n Error of b is {np.sqrt(b[1, 1])}')
	plt.show()
	return 0

data = data.loc[data['amp'] > .15 ]
data['time'] = data['time'] * 1000
data = data.loc[data['time'] > .062]


print(t2(data['time'], data['amp'], data['err']))



