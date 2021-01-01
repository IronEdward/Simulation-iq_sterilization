import pandas as pd

data = pd.read_csv("raw_datasets/WORLD-2019.csv")
data["T"] = data["M"] + data["F"]
data = data.drop(columns = ["M", "F"])
total_population = data.sum(axis = 0)["T"]
data["T"] = data["T"]/(total_population*5)

new_data = pd.DataFrame()

for index, row in data.iterrows():
    low, high = row["Age"].split("-")
    for age in range(int(low), int(high)+1):
        new_data = new_data.append([row["T"]], ignore_index = True)
        
new_data.to_csv("clean_datasets/age_distribution.txt", 
                index=False, header=False)