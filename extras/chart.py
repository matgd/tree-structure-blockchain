import csv

import numpy as np
import matplotlib.pyplot as plt

x_axis, y_axis = [], []

import sys

print('>>>')
print(sys.argv)

with open(f'{sys.argv[1]}_1.csv') as file:
    reader = csv.reader(file)
    x_axis_1, y_axis_1 = [], []
    for name, number, time_elapsed in reader:
        if name.startswith('DELETE_CHAIN_'):
            x_axis_1.append(int(number))
            y_axis_1.append(float(time_elapsed))

with open(f'{sys.argv[1]}_2.csv') as file:
    reader = csv.reader(file)
    x_axis_2, y_axis_2 = [], []
    for name, number, time_elapsed in reader:
        if name.startswith('DELETE_CHAIN_'):
            x_axis_2.append(int(number))
            y_axis_2.append(float(time_elapsed))

with open(f'{sys.argv[1]}_3.csv') as file:
    reader = csv.reader(file)
    x_axis_3, y_axis_3 = [], []
    for name, number, time_elapsed in reader:
        if name.startswith('DELETE_CHAIN_'):
            x_axis_3.append(int(number))
            y_axis_3.append(float(time_elapsed))

print('=' * 40)
print(x_axis_1)
for i in range(len(x_axis_1)):
    x_axis.append((x_axis_1[i] + x_axis_2[i] + x_axis_3[i]) / 3)
    y_axis.append((y_axis_1[i] + y_axis_2[i] + y_axis_3[i]) / 3)

z = np.polyfit(x_axis, y_axis, 1)
p = np.poly1d(z)
plt.ylim(0, 0.4)
plt.title('Time to append a new block to the chain')
plt.ylabel('Time [s]')
plt.xlabel('Number of block in the chain')
# plt.plot(x_axis, y_axis, '.') #
plt.plot(x_axis, y_axis, color='grey')
plt.plot(x_axis, p(x_axis), 'b--')
plt.show()
