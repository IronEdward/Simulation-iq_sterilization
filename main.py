from individual import *
from population import *

# Define threshold IQ
threshold_iq = 100
# Define population number
population_number = 1000
span = 100

# Generate populations for each IQ threshold
population = Population(population_number, threshold_iq)

for year in range(span):
    population.step(year)