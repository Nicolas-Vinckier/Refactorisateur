import os 

def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.read().splitlines()
        file2_lines = file2.read().splitlines()
        for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines), start=1):
            if line1 != line2:
                print(f"Line {i}:")
                print(f"{file1_path}: {line1}")
                print(f"{file2_path}: {line2}")
        print("Comparison complete.")

# Example usage:
compare_files("file1.txt", "file2.txt")

