import os
import shutil

# Task 3: Find files by extension
extension = ".txt"
txt_files = [f for f in os.listdir() if f.endswith(extension)]
print(f"Found text files: {txt_files}")

# Task 4: Move/copy files between directories
# Ensure 'test_dir' exists
if not os.path.exists("test_dir"):
    os.mkdir("test_dir")

if txt_files:
    shutil.move(txt_files[0], "test_dir/" + txt_files[0])
    print(f"Moved {txt_files[0]} to test_dir/")