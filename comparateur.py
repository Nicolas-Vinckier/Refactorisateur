import os

def compare_files(file1_path, file2_path):
    with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
        file1_lines = file1.read().splitlines()
        file2_lines = file2.read().splitlines()
        for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines), start=1):
            if line1 != line2:
                print(f"Line {i}:")
                print(f"{file1_path}: {line1}")
                print(f"{file2_path}: {line2}")
        print("Comparison complete.")

# Ask user for file paths
file1_path = input("Enter path for first file: ")
file2_path = input("Enter path for second file: ")

# Check if files exist
if not os.path.isfile(file1_path):
    print(f"{file1_path} does not exist.")
elif not os.path.isfile(file2_path):
    print(f"{file2_path} does not exist.")
else:
    # Compare files
    compare_files(file1_path, file2_path)
