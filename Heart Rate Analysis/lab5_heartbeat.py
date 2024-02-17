# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:18:37 2023

@author: Edwin
"""

import heartpy as hp
import matplotlib.pyplot as plt

sample_rate = 20000
data = hp.get_data("heartbeat.csv")

# Plot the original heart rate signal
plt.figure()
plt.plot(data)
plt.xlabel("Time (s)")
plt.ylabel("Heart rate (bpm)")
plt.title("Original Heart Rate Signal")
plt.show()

# Run the heart rate variability analysis
wd, m = hp.process(data, sample_rate)

# Plot the heart rate variability analysis results
plt.figure()
hp.plotter(wd, m)
plt.xlabel("Time (s)")
plt.ylabel("Heart rate (bpm)")
plt.title("Heart Rate Variability Analysis")
plt.show()

# Print the heart rate variability metrics
for measure in m.keys():
    print(f"{measure}: {m[measure]}")
