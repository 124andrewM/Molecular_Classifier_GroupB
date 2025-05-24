import os
import sys

# Example usage with python:
# python comma2space.py input_directory output_directory

# Description: this script runs through every file in the input directory
# replacing any commas with a space. This reformats the coordinates for viewing in
# molecular visualisation software.

if len(sys.argv) != 3:
    print("Usage: python comma_to_space.py <input_directory> <output_directory>")
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

# Make the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all CSV files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        # Construct the full input and output file paths
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".csv", ".txt"))
        # Open the input file for reading and the output file for writing
        with open(input_path, "r") as input, open(output_path, "w") as output:
            for line in input:
                # Replace each comme with a space and write to the output file
                output.write(line.replace(",", " "))

print(f"Converted all CSV files in {input_dir} to space-separated plain text files in {output_dir}.")