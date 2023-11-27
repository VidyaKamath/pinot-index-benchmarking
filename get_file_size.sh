#!/bin/bash

# Root directory containing tar.gz files
root_dir=$1

# Output file to store the command output
output_file=$2

# Loop through each tar.gz file in the root directory
for file in "$root_dir"/*.tar.gz; do
    if [ -f "$file" ]; then
        # Extract filename without extension
        filename=$(basename -- "$file")
        filename_noext="${filename%.*}"
        # Execute the command for each tar.gz file
		echo "Command executed for $filename_noext:" >> "$output_file"
        tar -vtf "$file" | grep star_tree_index  >> "$output_file"
		# tar -vtf "$file" | grep metadata.properties  >> "$output_file"
		echo "--------------------------" >> "$output_file"
        echo "Command executed for $filename_noext"
    fi
done
