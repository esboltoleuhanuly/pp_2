import shutil
import os

source = "sample.txt"
backup = "sample_backup.txt"

# Task 4: Copy and back up files using shutil
shutil.copy(source, backup)
print(f"Backup created: {backup}")

# Task 5: Delete files safely
# Deleting the backup to demonstrate
os.remove(backup)
print(f"Backup file '{backup}' deleted.")