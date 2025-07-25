import os
import json

# Define folder and file path
FOLDER_PATH = r"FILEPATH"
FILE_NAME = "db.json"
FILE_PATH = os.path.join(FOLDER_PATH, FILE_NAME)

# Ensure folder exists
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)
    print(f"[INIT] Folder created at {FOLDER_PATH}")

# Check if the JSON database file exists
if not os.path.isfile(FILE_PATH):
    with open(FILE_PATH, 'w') as f:
        json.dump({}, f)
    print(f"[INIT] Database created at {FILE_PATH}")
else:
    with open(FILE_PATH, 'r') as f:
        existing_data = json.load(f)
    print(f"[LOAD] Existing data loaded from {FILE_PATH}: {existing_data}")

# Utility function to load data
def _load_data():
    with open(FILE_PATH, 'r') as f:
        return json.load(f)

# Utility function to save data
def _save_data(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[SAVE] Data saved: {data}")

# Function to read from local storage
def read_local_storage(key):
    data = _load_data()
    value = data.get(key, None)
    print(f"[READ] Key: '{key}' => Value: {value}")
    return value

# Function to write to local storage
def write_local_storage(key, value, overwrite=False):
    data = _load_data()

    if key in data:
        if overwrite:
            print(f"[OVERWRITE] Key '{key}' exists. Overwriting...")
            data[key] = value
            _save_data(data)
        else:
            print(f"[SKIP] Key '{key}' already exists. Use overwrite=True to replace.")
    else:
        print(f"[WRITE] Adding new key '{key}' with value '{value}'")
        data[key] = value
        _save_data(data)

# Example usage (uncomment for testing):
# write_local_storage("user", "Alice")
# write_local_storage("user", "Bob", overwrite=False)
# write_local_storage("user", "Bob", overwrite=True)
# read_local_storage("user")
# a = input()