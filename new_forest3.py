import pandas as pd
import random
import math
from tqdm import tqdm

# Load the tree data
tree_df = pd.read_csv('newForest.csv')

# Load the cut trees data
cut_trees_df = pd.read_csv('cut_trees.csv')

# Load the species dataset
species_df = pd.read_csv('50000dataset.csv')

# Define the number of trees per hectare for each species group
trees_per_hectare = [50, 70, 100, 120, 80, 80]

# Define the diameter and height ranges for each diameter class
diameter_ranges = [[5, 15], [15, 30], [30, 45], [45, 60], [60, 250]]  # in centimeters
height_ranges = [[250, 550], [550, 1000], [1000, 1500]]  # in centimeters

# Define a function to calculate the distance between a tree and its crown center
def calculate_damage_crown(row):
    if row['Status'] == 'Cut':
        stem_height = row['Height (m)']
        cutting_angle = row['Cutting Angle']  # Assuming the angle is in degrees

        # Calculate crown coordinates
        crown_x = (stem_height + 5) * math.sin(math.radians(cutting_angle))
        crown_y = (stem_height + 5) * math.cos(math.radians(cutting_angle))

        # Calculate coordinates of the crown
        crown_x1 = row['Coordinate_X'] + crown_x
        crown_y1 = row['Coordinate_Y'] + crown_y
        
        # Calculate distance between tree and crown center
        distance = math.sqrt((crown_x1 - row['Coordinate_X'])**2 + (crown_y1 - row['Coordinate_Y'])**2)

        # Check if distance is less than or equal to 5m for damage crown
        return f'{distance:.2f}m'
    else:
        return 'N/A'

# Define a function to calculate the damage to the stem
def calculate_damage_stem(row):
    if row['Status'] == 'Cut':
        cutting_angle_rad = math.radians(row['Cutting Angle'])
        x = row['Coordinate_X']

        # Check if tangent of cutting_angle_rad is zero
        if math.tan(cutting_angle_rad) == 0:
            return None

        # Calculate y1, y2, and y3
        y1 = x / math.tan(cutting_angle_rad) + 1
        y2 = x / math.tan(cutting_angle_rad) - 1
        y3 = x / math.tan(cutting_angle_rad)

        # Check if y3 is between y1 and y2
        if y1 < y3 < y2:
            return None
        else:
            damage_stem = abs(float(f'{y3:.2f}'))
            return damage_stem
    else:
        return "N/A"
    
# Define a function to calculate the growth of the tree
def calculate_growth(d0):
    growth = [d0]
    for year in range(1, 31):
        if 5 <= growth[-1] < 15:
            increment = 0.4
        elif 15 <= growth[-1] < 30:
            increment = 0.5
        elif 30 <= growth[-1] < 45:
            increment = 0.6
        elif 45 <= growth[-1] < 60:
            increment = 0.5
        else:
            increment = 0.7
        growth.append(round(growth[-1] + increment, 2))
    return growth

# Define a function to calculate the production of the tree
def calculate_production(diameter):
    return round((0.2 + 2.5 * diameter**2), 2)

# Define a function to calculate the production of the tree after 30 years
def calculate_production_30(diameter):
    D = calculate_growth(round(diameter))[-1]
    return 0.0971 + 9.503 * D**2

# Define a function to calculate the diameter after 30 years based on growth rate
def calculate_diameter_growth(diameter):
    growth = diameter
    for _ in range(30):
        if 5 <= growth < 15:
            growth += 0.4
        elif 15 <= growth < 30:
            growth += 0.5
        elif 30 <= growth < 45:
            growth += 0.6
        elif 45 <= growth < 60:
            growth += 0.5
        else:
            growth += 0.7
    return round(growth, 2)

# Define a function to calculate the volume after 30 years based on species group
def calculate_volume_30(diameter_30, dip_non_dip):
    if dip_non_dip == 'Dip':
        if diameter_30 < 15:
            volume_30 = 0.022 + 3.4 * diameter_30**2
        else:
            volume_30 = -0.0971 + 9.503 * diameter_30**2
    else:  # NonDip
        if diameter_30 < 30:
            volume_30 = 0.03 + 2.8 * diameter_30**2
        else:
            volume_30 = -0.331 + 6.694 * diameter_30**2
    return round(volume_30, 2)

# Create a list to hold the generated data
tree_data = []

blockSizeX = 10
blockSizeY = 10
total_blocks = blockSizeX * blockSizeY
total_iterations = total_blocks * sum(trees_per_hectare)

# Initialize variable to count total trees generated
total_trees_generated = 0

# Loop through each block with a progress bar
for block_x in tqdm(range(1, blockSizeX + 1), desc="Blocks"):
    for block_y in tqdm(range(1, blockSizeY + 1), desc="Blocks Y", leave=False):
        # Initialize variables for counting the number of trees generated
        trees_generated = 0
        
        # Loop through each species group
        for species_group, trees_in_group in enumerate(trees_per_hectare, start=1):
            # Loop through each tree in the current species group
            for _ in range(trees_in_group):
                # Increment total trees generated
                total_trees_generated += 1
                
                # Increment tree number
                trees_generated += 1
                
                # Generate random diameter and height for the current tree
                diameter = random.uniform(diameter_ranges[0][0], diameter_ranges[-1][1])
                height = random.uniform(height_ranges[0][0], height_ranges[-1][1]) / 100

                # Calculate volume of the tree
                volume = 3.142 * round((diameter / 200) ** 2 * (height * 0.50), 2)

                # Determine status of the tree
                status = 'Cut' if diameter > 45 else 'Keep'

                # Generate random cutting angle (with decimal point)
                cutting_angle = round(random.uniform(0, 360), 1)
                
                # Get species code and species group corresponding to the current tree
                specode = species_df.iloc[total_trees_generated - 1]['SPECODE']
                species_group_name = species_df.iloc[total_trees_generated - 1]['SPECIES-GROUP']
                dip_non_dip = species_df.iloc[total_trees_generated - 1]['Dip/NonDip']

                # Generate x and y coordinates within the block (100x100) and convert to integers
                x = (block_x - 1) * 100 + int(random.uniform(0, 99))
                y = (block_y - 1) * 100 + int(random.uniform(0, 99))

                # Generate tree number in the format T0101XXXX
                tree_number = f"T{block_x:02d}{block_y:02d}{random.randint(1000, 9999)}"

                # Determine diameter class
                diameter_class = None
                for i, (low, high) in enumerate(diameter_ranges, start=1):
                    if low <= diameter < high:
                        diameter_class = i
                        break

                # Calculate the diameter and volume after 30 years of growth
                diameter_30 = calculate_diameter_growth(diameter)
                volume_30 = calculate_volume_30(diameter_30, dip_non_dip)

                # Append the tree information to the list, including block_x and block_y
                tree_data.append([
                    block_x, 
                    block_y, 
                    x, 
                    y, 
                    tree_number, 
                    specode, 
                    species_group_name, 
                    f'{diameter:.2f}', 
                    diameter_class, 
                    f'{height:.2f}', 
                    volume, 
                    status, 
                    calculate_production(diameter),  # Production
                    volume if status == 'Cut' else "", 
                    cutting_angle,
                    calculate_damage_crown({
                        'Status': status,
                        'Height (m)': height,
                        'Cutting Angle': cutting_angle,
                        'Coordinate_X': x,
                        'Coordinate_Y': y
                    }),
                    calculate_damage_stem({
                        'Status': status,
                        'Cutting Angle': cutting_angle,
                        'Coordinate_X': x
                    }),
                    calculate_growth(diameter)[-1],  # Add the diameter after 30 years of growth
                    calculate_production_30(diameter),  # Add the Production 30
                    diameter_30,  # Diameter after 30 years
                    volume_30,  # Volume after 30 years
                ])

                # Display progress
                current_iteration = (block_x - 1) * blockSizeX * sum(trees_per_hectare) + (block_y - 1) * sum(trees_per_hectare) + trees_generated
                progress = current_iteration / total_iterations * 100
                print(f'Progress: {progress:.2f}% ({current_iteration}/{total_iterations})', end='\r')

# Convert the list to a DataFrame and save it as a CSV file
output_df = pd.DataFrame(tree_data, columns=[
    'Block_X', 
    'Block_Y', 
    'Coordinate_X', 
    'Coordinate_Y', 
    'Tree_Number', 
    'SPECODE', 
    'SPECIES-GROUP', 
    'Diameter (cm)', 
    'Diameter Class', 
    'Height (m)', 
    'Volume (m^3)', 
    'Status', 
    'Production',
    'Cut Volume (m^3)', 
    'Cutting Angle', 
    'Damage Crown', 
    'Damage Stem', 
    'Diameter_30', 
    'Production_30', 
    'Diameter after 30 years', 
    'Volume after 30 years'
    
])

output_df.to_csv('newForest.csv', index=False)
print("\nTree data has been successfully generated and saved to 'newForest.csv'")
