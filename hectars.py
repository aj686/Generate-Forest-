import pandas as pd
import random

# Load the existing tree data
tree_df = pd.read_csv('newForest.csv')

# Define the number of trees per hectare for each species group
trees_per_hectare = [50, 70, 100, 120, 60, 60, 40]

# Define the number of trees to generate for each species group
total_trees_generated = sum(trees_per_hectare)

# Sample 500 trees randomly from the existing data
sampled_trees = tree_df.sample(n=total_trees_generated, replace=True)

# Reset the index of the sampled trees DataFrame
sampled_trees.reset_index(drop=True, inplace=True)

# Save the sampled trees data to a new CSV file
sampled_trees.to_csv('500_trees_data.csv', index=False)

print("Data for 500 trees per hectare has been successfully generated and saved to '500_trees_data.csv'")
