import os
import shutil
from pathlib import Path

# Define folders array based on Makefile folders
folders = [
    "PrtDockerLocalNetwork",
    "PrtRedisService",
    "PrtAttributionService",
    "PrtDocumentService",
    "PrtInferenceService",
    "PrtIndexingDomain",
    "PrtAISearch"
]

# for folder in folders:
#     print(folder)

remote_folder = "/Users/systems/Downloads/backup"

# Iterate through each folder
for folder in folders:
    # Walk through all subdirectories in the folder
    for root, dirs, files in os.walk(f"{remote_folder}/{folder}"):
        if '.env' in files:
            # print("works")
            env_file_path = os.path.join(root, '.env')
            abs_path = os.path.abspath(env_file_path)
            print(f"Absolute path: {abs_path}")
            # Create destination path by removing "backup/" prefix
            dest_path = abs_path.replace(f"{remote_folder}/", "", 1)
            print(f"Dest. path: {dest_path}")
            # Copy the .env file to destination
            shutil.copy2(abs_path, dest_path)
            print(f"Copied to: {dest_path}")
