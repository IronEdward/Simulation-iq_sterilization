"""Clean raw dataset and extract useful data."""
import pandas as pd

# Define path as static value
PATH = "raw_datasets/life_table.txt"

# Read raw dataset
data = pd.read_csv(PATH, delim_whitespace = True)
# Strip unnecessary columns (Needs to be done manually)
data = data.drop(
    columns = ["Year","Age" , "ax", "lx", "dx", "Lx", "Tx", "ex", "mx"])

# Create output file
data.to_csv("clean_datasets/clean_life_table.txt", index = False, header=False)