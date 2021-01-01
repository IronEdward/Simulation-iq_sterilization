import numpy as np
from individual import *
import matplotlib.pyplot as plt
import pandas as pd
from data import *
from random import choices

class Population():
    """Class for managing a population of population_number people."""
    # Static constants
    __iq_mean = 100
    __iq_standard_deviation = 15
    # Visualization-related
    __visualization_pause_time = 0.01
    __visualization_y_limit = 500
    __visualization_x_limit = 200
    __visualization_text_x = 10
    __visualization_test_y = __visualization_y_limit - 50
    # Arbitrary probability from past data
    __birth_probability = 0.5
    __legal_marriage_age = 18
    # randoIQFromGaussianDistribution * 0.6 + femaleIQ * 0.3 + maleIQ * 0.1
    __innate_iq_percentage = 0.6
    __mother_iq_percentage = 0.3
    __father_iq_percentage = 0.1
    
    # PATHs for reading data
    __DEATH_PATH = "data/clean_datasets/clean_life_table.txt"
    __MARRIAGE_PATH = "data/params/marriage_parameters.txt"
    __AGE_PATH = "data/clean_datasets/age_distribution.txt"
    
    def __init__(self, population_number, threshold_iq):
        """Generate population of population_number people."""
        # Load necessary datasets
        self.load_datasets()
        
        # Initialize instance variables
        self.population_number = population_number
        self.threshold_iq = threshold_iq
        
        self.generate_population()
    
    def step(self, year):
        """Step through one year."""
        # Print information to console
        print("YEAR: ", year, 
              "AVERAGE AGE: ", self.average_age(), 
              "POPULATION: ", len(self.population), 
              "AVERAGE IQ: ", self.average_iq())

        # Create a copy to keep track of original population array
        population_copy = list(self.population)
        # Loop through individuals
        for individual_index in range(len(population_copy)):
            # Get individual object
            individual = population_copy[individual_index]
            
            self.marriage_status(individual, individual_index)
            self.birth(individual, individual_index)
            self.life_status(individual, individual_index)
        # Run visualization for each step
        self.visualize_populational_iq(year)
    
    #?------------------------------Main Functions------------------------------
    #? Main functions are called each step.
    
    def marriage_status(self, individual, individual_index):
        """Generate marriages."""
        # Calculate marriage probability
        #! Argument number needs to be manually filled in
        # If the individual is 17 right now, they'll be 18 by the next step. 
        # So add them to the marriage array.
        if individual.age == 17:
            if individual.gender == "male":
                self.male_unmarried.append(individual)
            else:
                self.female_unmarried.append(individual)

        if np.random.random() <\
            objective(individual.age, self.popt[0], self.popt[1], self.popt[2])\
                and individual.couple == None\
                and (individual in self.male_unmarried\
                or individual in self.female_unmarried):
            # Generate opponent
            if individual.gender == "male":
                # If there are available unmarried females
                if(len(self.female_unmarried) > 1):
                    # Choose one unmarried female to be bride
                    opponent = np.random.randint(
                        0, len(self.female_unmarried)-1)
                    # Change couple status           
                    self.population[self.population.index(individual)].couple =\
                    self.female_unmarried[opponent]
                    # Change couple status for opponent
                    self.population[self.population.index(
                    self.female_unmarried[opponent])].couple =\
                    self.population[self.population.index(individual)]
                    # Remove both from unmarried list
                    self.male_unmarried.remove(individual)
                    self.female_unmarried.remove(self.female_unmarried[opponent])
            else:
                # If there are available unmarried males
                if(len(self.male_unmarried) > 1):
                    # Choose one unmarried male to be bride
                    opponent = np.random.randint(
                        0, len(self.male_unmarried)-1)
                    # Change couple status from None to one male
                    self.population[self.population.index(individual)].couple =\
                    self.male_unmarried[opponent]
                    # Change couple status for opponent
                    self.population[self.population.index(
                    self.male_unmarried[opponent])].couple =\
                    self.population[self.population.index(individual)]
                    # Remove male from unmarried list
                    self.female_unmarried.remove(individual)
                    self.male_unmarried.remove(self.male_unmarried[opponent])
                   
    def birth(self, individual, individual_index):
        """Generate children."""
        if np.random.random() < self.__birth_probability\
            and individual.can_have_baby == True\
            and individual.couple != None\
            and individual.child == False:
            # The couple cannot have any more children
            self.population[individual_index].child = True
            individual.couple.child = True
            
            # Create child
            if individual.gender == "male":
                gender, individual = self.generate_child(
                    individual.couple, individual)
            else:
                gender, individual = self.generate_child(
                    individual, individual.couple)
                
            # Append child to array
            self.population.append(individual)
    
    def life_status(self, individual, individual_index):
        """Calculate the likelihood of individual dying.
        """
        if np.random.random() <= self.life_table[individual.age]:
            # Kill (remove from list)
            self.population.remove(individual)
            if individual in self.male_unmarried:
                self.male_unmarried.remove(individual)
            elif individual in self.female_unmarried:
                self.female_unmarried.remove(individual)
        else:
            # Add 1 to age
            self.population[self.population.index(individual)].age += 1
    
    def visualize_populational_iq(self, year):
        """Create visualization of IQ distribution."""
        # If it's the first year, create a new window
        if year == 0:
            plt.figure()
        # Extract IQ values from self.population
        population_iq = [individual.iq for individual in self.population]
        # Plot population_iq
        plt.hist(population_iq, bins = 50)
        plt.gca().set(title='IQ Distribution', ylabel='Number of people')
        plt.ylim(0, self.__visualization_y_limit)
        plt.xlim(0, self.__visualization_x_limit)
        plt.text(self.__visualization_text_x, self.__visualization_test_y, 
                 "threshold: " + str(self.threshold_iq), fontsize=12)
        plt.draw()
        # Clear screen and pause for __visualization_pause_time
        plt.pause(self.__visualization_pause_time)
        plt.cla()
        
    #?-----------------------------Helper Functions-----------------------------
    #? Helper functions are tools used in main functions.
    
    def generate_population(self):
        """Generate population of population_number people. Returns array of 
        male_population and female_population.
        """
        # Initialize arrays for arrays
        self.male_population = []; self.female_population = []
        self.male_unmarried = []; self.female_unmarried = []
        # Create individuals
        for _ in range(self.population_number):
            gender, individual = self.generate_one_person()
            # Add individual to respective arrays depending on gender
            if gender == "male":
                self.male_population.append(individual)
                if individual.age >= self.__legal_marriage_age:
                    self.male_unmarried.append(individual)
            else:
                self.female_population.append(individual)
                if individual.age >= self.__legal_marriage_age:
                    self.female_unmarried.append(individual)
        # Compile total population
        self.population = list(self.male_population + self.female_population)
    
    def generate_one_person(self):
        """Generate one person. Returns individual() class of one individual.
        """
        # Sample gender with a 50% probability for each gender
        gender = ["male", "female"][np.random.randint(0, 2)]
        # Sample IQ for one individual from Gaussian (normal) distribution
        iq = float(np.random.normal(
            self.__iq_mean, self.__iq_standard_deviation, 1))
        age = choices([x for x in range(0, 100)], self.age_distribution)[0]
                
        # If the individual's IQ is lower than the threshold, the individual
        # cannot have children regardless of the sponse's IQ
        if iq <= self.threshold_iq:
            can_have_baby = False
        else:
            can_have_baby = True

        # Create person with given parameters and return gender and Individual
        return gender, Individual(gender, iq, age, can_have_baby)
    
    def generate_child(self, mother, father):
        """Generate child. Returns individual() class of child.
        """
        # Sample gender with a 50% probability for each gender
        gender = ["male", "female"][np.random.randint(0, 2)]
        # Generate IQ from parents' IQ and normal distribution
        iq = float(np.random.normal(
            self.__iq_mean, self.__iq_standard_deviation, 1) *\
            self.__innate_iq_percentage +\
            mother.iq * self.__mother_iq_percentage +\
            father.iq * self.__father_iq_percentage)
        
        # If the individual's IQ is lower than the threshold, the individual
        # cannot have children regardless of the sponse's IQ
        if iq <= self.threshold_iq:
            can_have_baby = False
        else:
            can_have_baby = True
        
        # Create person with given parameters and return gender and Individual
        return gender, Individual(gender, iq, 0, can_have_baby)
    
    def load_datasets(self):
        """Loads all necessary datasets."""
        # Generate lookup table for death probability of each age
        self.life_table = {}
        life_table_file = open(self.__DEATH_PATH, "r")
        for index, line in enumerate(life_table_file.readlines()):
            self.life_table[index] = float(line.replace("\n", ""))
            
        # Generate lookup function for marriage probability of each age
        self.popt = np.array(
            pd.read_csv(self.__MARRIAGE_PATH, header = None)[0])
        
        # Generate age distribution
        self.age_distribution = []
        age_distribution_file = open(self.__AGE_PATH, "r")
        for index, line in enumerate(age_distribution_file.readlines()):
            self.age_distribution.append(float(line.replace("\n", "")))

    def average_age(self):
        """Return average age of population."""
        age_sum = 0
        for individual in self.population:
            age_sum += individual.age
        return age_sum/len(self.population)
    
    def average_iq(self):
        """Calculate average IQ."""
        iq_sum = 0
        for individual in self.population:
            iq_sum += individual.iq
        return iq_sum/len(self.population)