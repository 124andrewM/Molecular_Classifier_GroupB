import os
import random
import csv
import sys

# An example input to run this script:
# python displace_coordinates.py input_dir output_dir 3.5

# This script takes in a directory of csv files containing atom xyz coordinates and 
# randomly moves a single coordinates for between 2 and 5 atoms in each file 
# where the total adjustments sum to the total displacement.

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]}: <input_molecules_path>, <output_molecules_path>, <total_displacement e.g 3.0 for 3.0 angstroms>")
    print("Note: Input directory should contain only the csv files to be modified")
    sys.exit()
else:
    csv_paths = os.path.join(os.getcwd(), sys.argv[1])
    output_directory =  sys.argv[2]
    total_distance = float(sys.argv[3])

# Function: choose_position
# Purpose: Randomly selects a coordinate to modify
def choose_position(number_of_atoms):
    return (random.randint(0,number_of_atoms-1), random.randint(0,2))

# Function: generate_random_floats
# Purpose: Generates a list of random floats that sum to a target displacement
def generate_random_floats(n, target_sum):
    nums = [random.random() for _ in range(n)]
    current_sum = sum(nums)
    # Normalise and scale the numbers around the desired max displacement
    scale = (target_sum / current_sum)
    scaled_nums = [x * scale for x in nums]
    return scaled_nums

# Get all the csv files in the input directory
file_names = os.listdir(csv_paths)

# Go through each file
for file in file_names:
    # Get the full input path for a csv file
    full_path = os.path.join(csv_paths, file)
    # Use the input path to generate the output path with "nonequilibrium_" prefix
    output_path = os.path.join(os.getcwd(), output_directory, f"nonequilibrium_{sys.argv[3].replace('.','')}_{file}")

    # Pull all the atom data out and store it in lists
    atoms, coords, atoms_changed = [], [], []

    # Read the input csv file
    with open(full_path, 'r', encoding='utf-8-sig') as f:
        # Go through each line in the file
        for line in f:
            # Remove any whitespace and split the line by commas
            line_split = line.strip().split(',')
            # Check if the line has an atom and 3 coordinates
            if len(line_split) != 4:
                print(f"Error: Line {line} in {full_path} did not contain exactly 4 values (atom and 3 coordinates). Skipping this line.")
            else:
                # Append the atom and coordinates to the respective lists
                atoms.append(line_split[0])
                coords.append([float(val) for val in line_split[1:]])
    
    # Choose a random number of atoms to modify between 2 and minimum of either 4 or the number of atoms
    number_of_changes = random.randint(2, min(len(atoms) + 1, 5))

    # Generate random floats that sum to the total dicplacement
    changes = generate_random_floats(number_of_changes, total_distance)

    # List to keep track of which coordinates have been changed
    positions_changed = []
    
    # Loop through the number of changes and randomly select a coordinate to modify
    for change in range(number_of_changes):
        # Choose a random xyz position to modify
        chosen_position = choose_position(len(atoms))
        # If the chosen position has already been changed, choose a new one
        while chosen_position in positions_changed:
            chosen_position = choose_position(len(atoms))
        # Add the position to the list of changed positions
        positions_changed.append(chosen_position)
        # Update the value for the chosen position
        coords[chosen_position[0]][chosen_position[1]] += changes[change]
    
    # Full list for the output data
    output = []

    # Go through all atoms and coordinates and append them to the output list
    for n in range(len(atoms)):
        tmp_list = []
        tmp_list.append(atoms[n])
        tmp_list.append(round(coords[n][0], 6))
        tmp_list.append(round(coords[n][1], 6))
        tmp_list.append(round(coords[n][2], 6))
        output.append(tmp_list)

    # Write the output data to a new csv file
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output)
    