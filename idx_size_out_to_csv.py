import os

ip_dir = "/home/vidyak2/raw_data/star_idx_size"

for root, dirs, files in os.walk(ip_dir):
    for file in files:
        if file.endswith(".out"):
            basename = file.split(".")[0]
            csv_file = basename + ".csv"
            csv_file_p = os.path.join(root, csv_file)
            csv_data = []
            with open(os.path.join(root, file), "r") as fp:
                lines = fp.readlines()
            for line in lines:
                if line.startswith("Command") or line.startswith("--"):
                    continue
                if line.startswith("-r"):
                    data = line.split()
                    size = data[2]
                    file = data[5]
                    csv_data.append(f"{file},{size}\n")
            
            with open (csv_file_p, "w") as fp:
                fp.write('"segment_name", "star_tree_size\n"')
                # fp.write('"segment_name", "metadata_properties_size\n"')
                for line in csv_data:
                    fp.write(line)
