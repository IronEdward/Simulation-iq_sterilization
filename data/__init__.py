"""Functions for data generation and manipulation."""
import numpy as np

# Objective function for marriage estimation
def objective(x, a, b, c):
    return 1 / (1 + np.exp(-a * (x - b))) + c