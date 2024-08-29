import os
import shutil
import hashlib
import json
from tqdm import tqdm

HASH_CACHE_FILE = "file_hashes.json"  # Change this to the path where you want to save the hash cache. Currently set to current folder


def compute_file_hash(file_path):
    # Computing SHA256 hash
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def load_hash_cache():
    # Load the hash cache from a JSON file.
    if os.path.exists(HASH_CACHE_FILE):
        with open(HASH_CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_hash_cache(hash_cache):
    # Save the hash cache to json
    with open(HASH_CACHE_FILE, "w") as f:
        json.dump(hash_cache, f)


def move_duplicate_files(source_path, destination_path):
    print("Starting Move-DuplicateFiles script...")
    print(f"SourcePath: {source_path}")
    print(f"DestinationPath: {destination_path}")

    if not os.path.exists(destination_path):
        print(f"Destination path does not exist. Creating {destination_path}")
        os.makedirs(destination_path)
    else:
        print(f"Destination path exists: {destination_path}")

    # Get all files
    print(f"Retrieving files from {source_path}")
    files = []
    for root, _, filenames in os.walk(source_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    if not files:
        print(f"No files found in {source_path}")
        return

    print(f"Found {len(files)} files in {source_path}")

    # Load existing hash cache
    hash_cache = load_hash_cache()

    # Compute hash for each file and group by hash
    print("Computing file hashes...")
    file_groups = {}
    for file in tqdm(files, desc="Computing hashes"):
        if file in hash_cache:
            file_hash = hash_cache[file]
        else:
            file_hash = compute_file_hash(file)
            hash_cache[file] = file_hash

        if file_hash not in file_groups:
            file_groups[file_hash] = []
        file_groups[file_hash].append(file)

    # Save updated hash cache
    save_hash_cache(hash_cache)

    # Iterate over each group of files with the same hash
    for file_hash, group in file_groups.items():
        if len(group) > 1:
            print(f"Found duplicate files with hash {file_hash}")
            # Keep the first file and move the rest
            files_to_move = group[1:]
            for file in files_to_move:
                destination_file_path = os.path.join(
                    destination_path, os.path.basename(file)
                )

                # Handle potential name collisions
                counter = 1
                while os.path.exists(destination_file_path):
                    base, ext = os.path.splitext(os.path.basename(file))
                    destination_file_path = os.path.join(
                        destination_path, f"{base}_{counter}{ext}"
                    )
                    counter += 1

                print(f"Moving {file} to {destination_file_path}")
                shutil.move(file, destination_file_path)

    print("Move-DuplicateFiles script completed.")


source_path = "/path/to/folder/containing/duplicate/files"
destination_path = "/path/to/folder/to/move/duplicate/files/to"
move_duplicate_files(source_path, destination_path)
