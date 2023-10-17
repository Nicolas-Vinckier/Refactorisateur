import filecmp
import os


def compare_folders(dir1, dir2):
    """
    Compare the contents of two directories and report differences.
    """
    dcmp = filecmp.dircmp(dir1, dir2)

    # Report files and subdirectories unique to dir1
    for item in dcmp.left_only:
        print(f"Only in {dir1}: {item}")

    # Report files and subdirectories unique to dir2
    for item in dcmp.right_only:
        print(f"Only in {dir2}: {item}")

    # Report files with differences
    for name in dcmp.diff_files:
        print(f"Different file: {name} in {dir1} and {dir2}")

    # Recursively compare subdirectories
    for sub_dcmp in dcmp.subdirs.values():
        compare_folders(sub_dcmp.left, sub_dcmp.right)


if __name__ == "__main__":
    folder1 = input("Enter path to the first folder: ")
    folder2 = input("Enter path to the second folder: ")

    # Check if paths exist and are directories
    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        print("One or both paths are not valid directories.")
        exit(1)

    compare_folders(folder1, folder2)
