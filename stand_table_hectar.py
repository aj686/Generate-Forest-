import pandas as pd

# Load the generated forest data
forest_df = pd.read_csv('500_trees_data.csv')

# Define diameter categories
diameter_categories = ['5-15 cm', '15-30 cm', '30-45 cm', '45-60 cm', '60-250 cm']

# Initialize dictionaries to hold total volume, total number of trees, and diameter counts for each species group
total_volume_dict = {}
total_trees_dict = {}
diameter_counts_dict = {category: [0] * 7 for category in diameter_categories}

# Read the 'Diameter (cm)' column
diameter_values = forest_df['Diameter (cm)']

# Determine the diameter category for each tree and count occurrences by species group
for idx, diameter in enumerate(diameter_values):
    species_group = forest_df.at[idx, 'SPECIES-GROUP']
    if 5 <= diameter < 15:
        diameter_counts_dict['5-15 cm'][species_group-1] += 1
    elif 15 <= diameter < 30:
        diameter_counts_dict['15-30 cm'][species_group-1] += 1
    elif 30 <= diameter < 45:
        diameter_counts_dict['30-45 cm'][species_group-1] += 1
    elif 45 <= diameter < 60:
        diameter_counts_dict['45-60 cm'][species_group-1] += 1
    else:
        diameter_counts_dict['60-250 cm'][species_group-1] += 1

# Group the data by species group
grouped_data = forest_df.groupby('SPECIES-GROUP')

# Iterate over each species group
for species_group, group_data in grouped_data:
    # Calculate total volume and total number of trees for the current species group
    total_volume = group_data['Volume (m^3)'].sum()
    total_trees = len(group_data)
    
    # Append total volume and total number of trees to the dictionaries
    total_volume_dict[species_group] = round(total_volume, 2)  # Round to two decimal points
    total_trees_dict[species_group] = total_trees

# Create DataFrame for total volume and total number of trees
total_volume_df = pd.DataFrame(list(total_volume_dict.items()), columns=['Species Group', 'Total Volume (m^3)'])
total_trees_df = pd.DataFrame(list(total_trees_dict.items()), columns=['Species Group', 'Total Number of Trees'])

# Create DataFrame for diameter counts by species group
diameter_counts_df = pd.DataFrame(diameter_counts_dict)
diameter_counts_df.insert(0, 'Species Group', range(1, 8))  # Insert species group column

# Merge the DataFrames on the 'Species Group' column
merged_df = total_volume_df.merge(total_trees_df, on='Species Group').merge(diameter_counts_df, on='Species Group')

# Save the merged DataFrame to a single CSV file
merged_df.to_csv('forest_statistics.csv', index=False)

print("Successfully saved forest_statistics.csv.")
