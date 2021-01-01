"""Uses linear regression to generate probability of marriage for each age."""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from __init__ import *

# Define path as static value
PATH = "raw_datasets/Share-of-men-that-are-married-by-cohort-England-and-Wales-ONS.csv"

# Read raw dataset
data = pd.read_csv(PATH)

# Count number of data points for each year
year_count = {}
for index, row in data.iterrows():
    if row["Year"] not in year_count.keys():
        year_count[row["Year"]] = 0
    else:
        year_count[row["Year"]] += 1

# Sort dictionary by value
year_count = dict(sorted(year_count.items(), key = lambda item: item[1]))

# Get data of year with most age data
data = data[data.Year == list(year_count.keys())[-1]].drop(columns = ["Year"]) 
# Reset indexes
data = data.reset_index().drop(columns = ["index"])

# Transform data points
X = np.array(data["Age"])
y = np.array(data["Married"]) / 100 # Convert to percentage (0 <= value <= 1)

# Fit sigmoid curve to graph
popt, pcov = curve_fit(objective, X, y, method='dogbox')

"""--------------------------------For testing-------------------------------"""
# Generate test samples
test_X = np.array([value for value in range(18, 100)])
test_y = objective(test_X, popt[0], popt[1], popt[2])

# Plot outputs
plt.scatter(X, y, color="black")
plt.plot(test_X, test_y, color="blue")

# Show plot
plt.show()
"""--------------------------------End testing-------------------------------"""
# Save parameters

popt = pd.DataFrame(popt)
popt.to_csv("params/marriage_parameters.txt", index = False, header = False)