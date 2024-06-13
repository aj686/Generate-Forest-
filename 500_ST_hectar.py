import pandas as pd

# Load the generated forest data
forest_df = pd.read_csv('newForest.csv')

# Group the data by species group
grouped_data = forest_df.groupby('SPECIES-GROUP')

# Initialize dictionaries to hold aggregated data
total_volume_dict = {}
total_production_dict = {}
total_damage_crown_dict = {}
total_damage_stem_dict = {}
total_diameter_30_dict = {}
total_production_30_dict = {}

# Iterate over each species group
for species_group, group_data in grouped_data:
    # Calculate total volume for the current species group
    total_volume = group_data['Volume (m^3)'].sum()
    total_volume_dict[species_group] = round(total_volume, 2)  # Round to two decimal points

    # Calculate total production for the current species group
    total_production = group_data['Production'].sum()
    total_production_dict[species_group] = total_production

    # Calculate total damage to crown for the current species group
    total_damage_crown = group_data['Damage Crown'].apply(lambda x: 0 if x == 'N/A' else float(x.rstrip('m')) if isinstance(x, str) else x).sum()
    total_damage_crown_dict[species_group] = total_damage_crown

    # Calculate total damage to stem for the current species group
    total_damage_stem = group_data['Damage Stem'].apply(lambda x: 0 if x == 'N/A' else float(x)).sum()
    total_damage_stem_dict[species_group] = total_damage_stem

    # Calculate total diameter after 30 years for the current species group
    total_diameter_30 = group_data['Diameter after 30 years'].sum()
    total_diameter_30_dict[species_group] = total_diameter_30

    # Calculate total production after 30 years for the current species group
    total_production_30 = group_data['Production_30'].sum()
    total_production_30_dict[species_group] = total_production_30

# Create DataFrames from the dictionaries
total_volume_df = pd.DataFrame(list(total_volume_dict.items()), columns=['Species Group', 'Total Volume (m^3)'])
total_production_df = pd.DataFrame(list(total_production_dict.items()), columns=['Species Group', 'Total Production'])
total_damage_crown_df = pd.DataFrame(list(total_damage_crown_dict.items()), columns=['Species Group', 'Total Damage Crown (m)'])
total_damage_stem_df = pd.DataFrame(list(total_damage_stem_dict.items()), columns=['Species Group', 'Total Damage Stem'])
total_diameter_30_df = pd.DataFrame(list(total_diameter_30_dict.items()), columns=['Species Group', 'Total Diameter after 30 years'])
total_production_30_df = pd.DataFrame(list(total_production_30_dict.items()), columns=['Species Group', 'Total Production after 30 years'])

# Merge DataFrames on 'Species Group' column
merged_df = total_volume_df.merge(total_production_df, on='Species Group') \
    .merge(total_damage_crown_df, on='Species Group') \
    .merge(total_damage_stem_df, on='Species Group') \
    .merge(total_diameter_30_df, on='Species Group') \
    .merge(total_production_30_df, on='Species Group')

# Save the merged DataFrame to a single CSV file
merged_df.to_csv('500_stand_table.csv', index=False)

print("Successfully saved 500_stand_table.csv.")
