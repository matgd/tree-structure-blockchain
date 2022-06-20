import csv
import sys

import numpy as np
import matplotlib.pyplot as plt

x_axis, y_axis = [], []
x_s, y_s = [], []

input_file = sys.argv[1]
if not input_file: 
    raise FileNotFoundError('Provide filename as argument (must end with "_1.csv")')

total_chains = 2**20 - 1  # 1 (empty participant chain, metadata)
time_vals = []

def seconds_to_microseconds(seconds: float):  # μs
    return seconds * 1_000_000;

for i in range(3):
    with open(input_file.replace('_1.csv', f'_{i+1}.csv')) as file:
        reader = csv.reader(file)
        x_s.append([])
        y_s.append([])
        print(file.name)
        for name, number, time_elapsed in reader:
            if name.startswith('DELETE_CHAIN_'):
                total_chains -= 1
                x_s[i].append(total_chains)
                y_s[i].append(seconds_to_microseconds(float(time_elapsed)))
                time_vals.append((time_elapsed, name.replace('Participant(', '').replace('DELETE_CHAIN_', '').replace(')', '')))

for i in range(len(x_s[0])):
    sum_y = 0
    for j in range(len(x_s)):
        sum_y += y_s[j][i]

    x_axis.append(x_s[0][i])
    y_axis.append((sum_y) / len(y_s))

z = np.polyfit(x_axis, y_axis, 1)
p = np.poly1d(z)
plt.ylim(0, seconds_to_microseconds(0.00005))
plt.title('Time to delete X-th subchain (excluding no-participant subchain)')
plt.ylabel('Time [μs]')
plt.xlabel('Total subchains')
plt.ticklabel_format(style='plain')
plt.plot(x_axis, y_axis, '.')
plt.plot(x_axis, y_axis, color='grey')
plt.plot(x_axis, p(x_axis), 'b--')

print('Sorting...')
print('=' * 70)
from pprint import pprint
pprint(sorted(time_vals, reverse=True)[:20])

plt.show()
