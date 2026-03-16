import os

# Task 1: Create nested directories
dir_path = "parent/child/grandchild"
os.makedirs(dir_path)
print(f"Created nested directory: {dir_path}")

# Task 2: List files and folders
current_dir = os.getcwd()
print(f"Items in {current_dir}:")
for item in os.listdir(current_dir):
    print(f" - {item}")