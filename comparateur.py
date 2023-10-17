import filecmp
import os
import difflib
import datetime

BLACKLISTED_EXTENSIONS = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".mp4"}


def log(message):
    """
    Custom logging function to print to console and write to the log file.
    """
    print(message)
    with open(log_filename, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


def compare_files(file1, file2):
    """
    Compare two files and print line-by-line differences.
    """
    with open(file1, "r", encoding="utf-8", errors="ignore") as f1, open(
        file2, "r", encoding="utf-8", errors="ignore"
    ) as f2:
        # Read lines
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Get differences using difflib
    d = difflib.Differ()
    diff_iter = iter(list(d.compare(lines1, lines2)))

    for line in diff_iter:
        if line.startswith("- "):
            next_line = next(diff_iter, "")  # Get the next line from the iterator
            # If the next line starts with '+ ' and is just a space-adjusted version of the current line, skip both
            if (
                next_line.startswith("+ ")
                and next_line[2:].lstrip() == line[2:].lstrip()
            ):
                continue
            else:
                log(f"In {file1}, line removed: {line[2:].rstrip()}")
        elif line.startswith("+ ") and line[2:].strip(): 
            log(f"In {file2}, line added: {line[2:].rstrip()}")


def compare_folders(dir1, dir2):
    """
    Compare the contents of two directories and report differences.
    """
    dcmp = filecmp.dircmp(dir1, dir2)

    # Report files and subdirectories unique to dir1
    for item in dcmp.left_only:
        if not item.endswith(tuple(BLACKLISTED_EXTENSIONS)):
            log(f"Only in {dir1}: {item}")

    # Report files and subdirectories unique to dir2
    for item in dcmp.right_only:
        if not item.endswith(tuple(BLACKLISTED_EXTENSIONS)):
            log(f"Only in {dir2}: {item}")

    # Compare files with differences
    for name in dcmp.diff_files:
        if not name.endswith(tuple(BLACKLISTED_EXTENSIONS)):
            log(f"Different file: {name}")
            compare_files(os.path.join(dir1, name), os.path.join(dir2, name))

    # Recursively compare subdirectories
    for sub_dcmp in dcmp.subdirs.values():
        compare_folders(sub_dcmp.left, sub_dcmp.right)


if __name__ == "__main__":
    folder1 = input("Entrer le nom du premier dossier: ")
    folder2 = input("Entrer le nom du second dossier: ")

    # Check if paths exist and are directories
    if not os.path.isdir(folder1) or not os.path.isdir(folder2):
        log("One or both paths are not valid directories.")
        exit(1)

    # Generate a unique timestamped log filename
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    log_filename = f"{current_time}-LOG.txt"

    # Begin directory comparison
    compare_folders(folder1, folder2)
