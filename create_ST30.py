import pandas as pd

# Load the first 500 rows of the generated forest data
forest_df = pd.read_csv('newForest.csv', nrows=500)

# Group the data by species group
grouped_data = forest_df.groupby('SPECIES-GROUP')

# Initialize dictionaries to hold aggregated data
total_volume_dict = {}
total_production_dict = {}
total_damage_dict = {}
total_growth30_dict = {}
total_production_30_dict = {}

# Iterate over each species group
for species_group, group_data in grouped_data:
    # Calculate total volume for the current species group
    total_volume = group_data['Volume (m^3)'].sum()
    total_volume_dict[species_group] = total_volume

    # Calculate total production for the current species group
    total_production = group_data['Production'].sum()
    total_production_dict[species_group] = total_production

    # Calculate total damage for the current species group
    total_damage = group_data['Damage Stem'].apply(lambda x: 0 if x == 'N/A' else float(x)).sum()
    total_damage_dict[species_group] = total_damage

    # Calculate total growth after 30 years for the current species group
    total_growth30 = group_data['Diameter after 30 years'].sum()
    total_growth30_dict[species_group] = total_growth30

    # Calculate total production after 30 years for the current species group
    total_production_30 = group_data['Production_30'].sum()
    total_production_30_dict[species_group] = total_production_30

# Create DataFrames from the dictionaries
total_volume_df = pd.DataFrame(list(total_volume_dict.items()), columns=['Species Group', 'Total Volume (m^3)'])
total_production_df = pd.DataFrame(list(total_production_dict.items()), columns=['Species Group', 'Total Production'])
total_damage_df = pd.DataFrame(list(total_damage_dict.items()), columns=['Species Group', 'Total Damage'])
total_growth30_df = pd.DataFrame(list(total_growth30_dict.items()), columns=['Species Group', 'Growth30'])
total_production_30_df = pd.DataFrame(list(total_production_30_dict.items()), columns=['Species Group', 'Production30'])

# Merge DataFrames on 'Species Group' column
merged_df = total_volume_df.merge(total_production_df, on='Species Group') \
    .merge(total_damage_df, on='Species Group') \
    .merge(total_growth30_df, on='Species Group') \
    .merge(total_production_30_df, on='Species Group')

# Round the values to 2 decimal points
merged_df = merged_df.round(2)

# Save the merged DataFrame to a single CSV file
merged_df.to_csv('stand_table_30.csv', index=False)

print("Successfully saved stand_table_30.csv.")
