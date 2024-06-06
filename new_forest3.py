import pandas as pd
import random
import math

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

# Define function to calculate damage crown
def calculate_damage_crown(row):
  if row['Status'] == 'Cut':
    stem_height = row['Height (m)']
    cutting_angle = row['Cutting Angle']  # Assuming the angle is in degrees

    # Calculate crown coordinates
    crown_x = (stem_height + 5) * math.sin(math.radians(cutting_angle))
    crown_y = (stem_height + 5) * math.cos(math.radians(cutting_angle))

    # Calculate tree coordinates (assuming columns are named 'Coordinate_X' and 'Coordinate_Y')
    tree_x = row['Coordinate_X']
    tree_y = row['Coordinate_Y']

    # Calculate distance between tree and crown center
    distance = math.sqrt((crown_x - tree_x)**2 + (crown_y - tree_y)**2)

    # Check if distance is less than or equal to 5m for damage crown
    return 'Damage Crown' if distance <= 5 else ''
  return ''  # Return empty string if not cut

# Create a list to hold the generated data
tree_data = []

blockSizeX = 10
blockSizeY = 10
total_blocks = blockSizeX * blockSizeY
total_iterations = total_blocks * sum(trees_per_hectare)

# Initialize variable to count total trees generated
total_trees_generated = 0

# Loop through each block
for block_x in range(1, blockSizeX + 1):
    for block_y in range(1, blockSizeY + 1):
        # Check if total trees generated reached 10 times
        if total_trees_generated >= 10 * sum(trees_per_hectare):
            break  # Stop the loop if 10 times the trees have been generated
        
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
                volume = 3.142 * (diameter / 200) ** 2 * (height * 0.50) / 1000000  # Convert to cubic meters

                # Determine status of the tree
                status = 'Cut' if diameter > 45 else 'Keep'

                # Generate random cutting angle (with decimal point)
                cutting_angle = round(random.uniform(0, 360), 1)
                
                # Get species code and species group corresponding to the current tree
                specode = species_df.iloc[total_trees_generated - 1]['SPECODE']
                species_group_name = species_df.iloc[total_trees_generated - 1]['SPECIES-GROUP']

                # Generate x and y coordinates within the block (100x100) and convert to integers
                x = int((block_x - 1) * 100 + random.uniform(0, 100))
                y = int((block_y - 1) * 100 + random.uniform(0, 100))

                # Generate tree number in the format T0101XXXX
                tree_number = f"T{block_x:02d}{block_y:02d}{random.randint(1000, 9999)}"

                # Determine diameter class
                diameter_class = None
                for i, (low, high) in enumerate(diameter_ranges, start=1):
                    if low <= diameter < high:
                        diameter_class = i
                        break
                # Determine production based on the status of the tree
                production = 'Victim' if status == 'Cut' else ''

                # Append the tree information to the list, including block_x and block_y
                tree_data.append([block_x, block_y, x, y, tree_number, specode, species_group_name, f'{diameter:.2f}', diameter_class, f'{height:.2f}', volume, status, "Cut" if status == 'Cut' else "", cutting_angle, calculate_damage_crown])


                
                # Display progress
                current_iteration = (block_x - 1) * blockSizeX * sum(trees_per_hectare) + (block_y - 1) * sum(trees_per_hectare) + trees_generated
                progress = current_iteration / total_iterations * 100
                print(f'Progress: {progress:.2f}% ({current_iteration}/{total_iterations})', end='\r')

    
# Apply the function to calculate damage crown and add the result as a new column
tree_df['Damage Crown'] = tree_df.apply( calculate_damage_crown, axis=1)
# Print the DataFrame to check if the 'Damage Crown' column is added
print(tree_df)
# Convert the list to a DataFrame
tree_df = pd.DataFrame(tree_data, columns=["Block_X", "Block_Y", "Coordinate_X", "Coordinate_Y", "Tree Number", "SPECODE", "SPECIES-GROUP", "Diameter (cm)", "Diameter Class", "Height (m)", "Volume (m^3)", "Status", "Production", "Cutting Angle", "Damage Crown"])

# Save the DataFrame to a CSV file
tree_df.to_csv('cut_trees.csv', index=False)

# Save the DataFrame to a CSV file
tree_df.to_csv('newForest.csv', index=False)

print("\nSuccessful")