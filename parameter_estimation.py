import pandas as pd
from scipy.optimize import curve_fit
import math
import numpy as np
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
import random


def model(x, a, b):
    return a + b * x


data = pd.read_excel('./FittsLaw_results.xlsx')
data = data[['mouseX','size','distance','time']]

# Effective target width
mouse_std = data.groupby(['size']).apply(np.std)['mouseX']
conditionlist = [(data['size']==20), (data['size']==40), (data['size']==60)]
choicelist = np.array(mouse_std) * 4.133
data['effective target width'] = np.select(conditionlist, choicelist)
data['IDe'] = [math.log2(d/s + 1) for (s,d) in zip(data['effective target width'], data['distance'])]
result_data_E = data.groupby(['effective target width', 'distance']).mean()[['time','IDe']]

poptE, pcovE = curve_fit(model, np.array(result_data_E['IDe']), np.array(result_data_E['time']))

# No effective target width
data['ID'] = [math.log2(d/s + 1) for (s,d) in zip(data['size'], data['distance'])]
result_data = data.groupby(['size', 'distance']).mean()[['time','ID']]

popt, pcov = curve_fit(model, np.array(result_data['ID']), np.array(result_data['time']))



ss_tot = sum((np.array(result_data_E['time'])-np.mean(result_data_E['time']))**2)
ss_res = sum((np.array(result_data_E['time'])-model(np.array(result_data_E['IDe']),poptE[0],poptE[1]))**2)

# R_Squared and Adjusted_R_squared
r_squared_E = 1 - (ss_res/ss_tot)

p = 1
n = 360
adjusted_r_E = 1 - (1-r_squared_E)*(n-1)/(n-p-1)

# Residual plot
residual = np.array(data['time']) - model(np.array(data['ID']),popt[0],popt[1])
fig, ax = plt.subplots(figsize=(9,7.5))
plt.scatter(data['ID'], residual, s=3)
plt.xlabel('X')
plt.ylabel('Residual')
plt.savefig('residual_plot')

# Bootstrapping
X_and_Y = list(zip(data['ID'], data['time']))
A = []
B = []
for i in range(1000):
    sample = np.random.choice(range(360), 360, replace=True)
    popt, pcov = curve_fit(model, [X_and_Y[i][0] for i in sample], [X_and_Y[i][1] for i in sample])
    A.append(popt[0])
    B.append(popt[1])

CI_a = (np.mean(A)-1.96*np.std(A)/math.sqrt(360), np.mean(A)+1.96*np.std(A)/math.sqrt(360)) # 95%
CI_b = (np.mean(B)-1.96*np.std(B)/math.sqrt(360), np.mean(B)+1.96*np.std(B)/math.sqrt(360)) # 95%


# K-fold
k = 5
idx = list(range(360))
random.shuffle(idx)
k1 = idx[:72]
k2 = idx[72:72*2]
k3 = idx[72*2:72*3]
k4 = idx[72*3:72*4]
k5 = idx[72*4:]

param_a = []
param_b = []
mae = []
for i in range(k):
    K = [k1, k2, k3, k4, k5]
    test = K[i]
    K.remove(K[i])
    K = sum(K, [])
    popt, pcov = curve_fit(model, [X_and_Y[i][0] for i in K], [X_and_Y[i][1] for i in K])
    param_a.append(popt[0])
    param_b.append(popt[1])
    error = np.array([X_and_Y[i][1] for i in test]) - model(np.array([X_and_Y[i][0] for i in test]), popt[0], popt[1])
    mae.append(abs(error))
print(np.mean(mae))
print(np.mean(param_a))
print(np.mean(param_b))


# data plot
fig, ax = plt.subplots(figsize=(9,7.5))
plt.scatter(data['ID'], data['time'], s=4)
plt.plot(data['ID'], model(data['ID'], popt[0], popt[1]), color='r')
plt.xlabel('ID')
plt.ylabel('TCT')
plt.savefig('data_plot')
