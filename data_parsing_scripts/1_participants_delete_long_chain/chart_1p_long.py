import csv
import sys

import numpy as np
import matplotlib.pyplot as plt

x_axis, y_axis = [], []
x_s, y_s = [], []

input_file = sys.argv[1]
if not input_file: 
    raise FileNotFoundError('Provide filename as argument (must end with "_1.csv")')


def seconds_to_microseconds(seconds: float):  # μs
    return seconds * 1_000_000;

for i in range(3):
    with open(input_file.replace('_1.csv', f'_{i+1}.csv')) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        x_s.append([])
        y_s.append([])
        for chain_length_entry, time_elapsed in reader:
            chain_length = int(chain_length_entry.split('_')[-1])
            x_s[i].append(chain_length)
            y_s[i].append(seconds_to_microseconds(float(time_elapsed)))

for i in range(len(x_s[0])):
    sum_y = 0
    for j in range(len(x_s)):
        sum_y += y_s[j][i]

    x_axis.append(x_s[0][i])
    y_axis.append((sum_y) / len(y_s))

z = np.polyfit(x_axis, y_axis, 1)
p = np.poly1d(z)
plt.ylim(0, seconds_to_microseconds(0.00016))
plt.title('Time to delete X-long subchain')
plt.ylabel('Time [μs]')
plt.xlabel('Subchain length')
plt.ticklabel_format(style='plain')
plt.plot(x_axis, y_axis, '.')
plt.plot(x_axis, y_axis, color='grey')
plt.plot(x_axis, p(x_axis), 'b--')

plt.show()
