import os
import time
from config import tags_file, timestamp_file

def load_existing_tags():
    if os.path.exists(tags_file):
        with open(tags_file, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_tags(tags):
    with open(tags_file, "w") as f:
        f.write("\n".join(sorted(tags)))

def load_last_run_timestamp():
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as f:
            return float(f.read().strip())
    return 0  # Return 0 if the file doesn't exist (indicating no previous run)

def save_current_timestamp():
    with open(timestamp_file, "w") as f:
        f.write(str(time.time()))