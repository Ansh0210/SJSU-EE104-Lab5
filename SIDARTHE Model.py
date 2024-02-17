# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:18:56 2023

@author: Nathan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# Set model parameters
N = 10000       # Total population
I1 = 1         # Initial infected
R1 = 0          # Initial recovered
D1 = 0          # Initial deceased
A1 = 0          # Initial asymptomatic
beta = 0.2      # Infection rate
alpha = 0.05    # Incubation rate
gamma = 0.08     # Recovery rate
delta = 0.03    # Death rate
epsilon = 0.05  # Asymptomatic rate

# How changes in the model parameters will change the plot:
# Increasing beta will cause the peak of the infected curve to be higher and earlier, and will also cause the total number of infected people to be higher.
# Increasing alpha will cause the peak of the infected curve to be earlier, but will not affect the total number of infected people.
# Increasing gamma will cause the peak of the infected curve to be earlier, and will also cause the total number of infected people to be lower.
# Increasing delta will cause the peak of the deceased curve to be higher and earlier, and will also cause the total number of deceased people to be higher.
# Increasing epsilon will cause the peak of the asymptomatic curve to be higher and earlier, and will also cause the total number of asymptomatic people to be higher.

# Define the model function
def SIDA(y, t, N, beta, alpha, gamma, delta, epsilon):#takes in the currently infected and rate of change
    S, I, D, A, R = y#split the variable to individuals
    dSdt = -beta*S*I/N #always decreases from max
    dIdt = beta*S*I/N - alpha*I #increases from susceptible but decreases due to death and recovery
    dDdt = delta*I #increases due to infected
    dAdt = epsilon*I - gamma*A #increases due to infected and decreases due to recovery
    dRdt = gamma*A #increases due to infected
    return dSdt, dIdt, dDdt, dAdt, dRdt#returns the rate of change of the variables

y1 = N-I1-R1-D1-A1, I1, D1, A1, R1 #compresses the data into one variable
t = np.linspace(0, 365, 365)#X axis 365 days to represent a year

sol = odeint(SIDA, y1, t, args=(N, beta, alpha, gamma, delta, epsilon))#Set up as Differential Equation and solve for X
S, I, D, A, R = sol.T  #split the Results from the solution 

# Plotting the results
fig, ax = plt.subplots()
ax.plot(t, S, 'b', label='Susceptible')
ax.plot(t, I, 'r', label='Infected')
ax.plot(t, D, 'g', label='Deceased')
ax.plot(t, A, 'y', label='Asymptomatic')
ax.plot(t, R, 'm', label='Recovered')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Number of individuals')
ax.set_ylim([0, N])
ax.legend()
plt.show()
