import csv
import re
import os

# Directory containing your files
idx_name = "1g_star_idx"
directory = f'/tmp/data/index_map/{idx_name}'  # Update this with the directory path

# Initialize a dictionary to store sizes for each property
property_sizes = {}

# Iterate through files in the directory
for filename in os.listdir(directory):
    if filename.endswith("star_tree_index_map"):  # Assuming all files have .txt extension
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r') as file:
            data = file.read()

        # Extracting lines containing ".size" and parsing them
        pattern = re.compile(r'^(.*\.SIZE)\s+=\s+(\d+)$', re.MULTILINE)
        matches = re.findall(pattern, data)

        # Storing sizes for each property in the dictionary
        for match in matches:
            prop = match[0]
            size = int(match[1])

            if prop not in property_sizes:
                property_sizes[prop] = []

            property_sizes[prop].append(size)

# Writing to CSV
csv_filename = f'/tmp/data/index_map/csv_out/{idx_name}_star_index_map_sizes_server1.csv'

with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Property', 'Sizes'])  # Writing header

    # Writing property and corresponding sizes to CSV
    for prop, sizes in property_sizes.items():
        writer.writerow([prop, ', '.join(map(str, sizes))])

print(f"CSV file '{csv_filename}' created successfully.")
