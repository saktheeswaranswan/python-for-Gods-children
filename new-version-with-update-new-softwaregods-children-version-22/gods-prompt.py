import os

# Target folder
folder_path = r"C:\Users\RITS\Desktop\flowchart-ai-9\new-softwaregods-children-version-2"
output_file = os.path.join(folder_path, "png_files_list.txt")

# List to store .png file paths
png_files = []

# Traverse the directory
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower().endswith('.png'):
            full_path = os.path.join(root, file)
            png_files.append(full_path)

# Write to output file
with open(output_file, 'w') as f:
    for path in png_files:
        f.write(f"{path}\n")

print(f"PNG files exported to: {output_file}")
