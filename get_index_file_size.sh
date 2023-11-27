#!/bin/bash

# Directory where the extracted folders are located
extracted_dir="/tmp/data/pinotServerData/tpch_lineitem_10g_sort_idx_OFFLINE"

# Directory to store index_map files
output_dir="/tmp/data/index_map/10g_sort_idx"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through all extracted folders
for folder in "$extracted_dir"/*; do
    if [ -d "$folder" ]; then
        # Get the base folder name
        base_folder=$(basename "$folder")
        
        # Check if the index_map file exists in the folder
        if [ -f "$folder/v3/index_map" ]; then
            # Copy the index_map file to the output directory with a modified name
            cp "$folder/v3/index_map" "$output_dir/${base_folder}_index_map"
            echo "Copied index_map from $folder to $output_dir/${base_folder}_index_map"
        else
            echo "index_map not found in $folder"
        fi
    fi
done
