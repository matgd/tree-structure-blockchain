import csv
import sys

import numpy as np
import matplotlib.pyplot as plt

x_axis, y_axis = [], []
x_s, y_s = [], []

input_file = sys.argv[1]
if not input_file: 
    raise FileNotFoundError('Provide filename as argument (must end with "_1.csv")')

for i in range(3):
    with open(input_file.replace('_1.csv', f'_{i+1}.csv')) as file:
        reader = csv.reader(file)
        x_s.append([])
        y_s.append([])
        print(file.name)
        for name, number, time_elapsed in reader:
            if name.startswith('DELETE_CHAIN_'):
                x_s[i].append(int(number))
                y_s[i].append(float(time_elapsed))

for i in range(len(x_s[0])):
    sum_x, sum_y = 0, 0
    for j in range(len(x_s)):
        sum_x += x_s[j][i]
        sum_y += y_s[j][i]

    x_axis.append((sum_x) / len(x_s))
    y_axis.append((sum_y) / len(y_s))

z = np.polyfit(x_axis, y_axis, 1)
p = np.poly1d(z)
plt.ylim(0, 0.4)
plt.title('Time to append a new block to the chain')
plt.ylabel('Time [s]')
plt.xlabel('Number of block in the chain')
plt.plot(x_axis, y_axis, '.')
plt.plot(x_axis, y_axis, color='grey')
plt.plot(x_axis, p(x_axis), 'b--')
plt.show()
