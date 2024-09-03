# src/file_utils.py
import os
from typing import Set
import time
from config import tags_file, timestamp_file, logger
import os 
def get_existing_tags() -> Set[str]:
    if os.path.exists(tags_file):
        with open(tags_file, "r") as f:
            return set(f.read().splitlines())
    else:
        return set()

def save_tags(tags: Set[str]) -> None:
    logger.info(f"Saving tags: {tags}")
    if not os.path.exists(tags_file):
        with open(tags_file, "w") as f:
            f.write("\n".join(sorted(tags)))
    with open(tags_file, "w") as f:
        f.write("\n".join(sorted(tags)))

def get_last_run_timestamp() -> float:
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as f:
            return float(f.read())
    else:
        return 0.0

def update_timestamp():
    if not os.path.exists(timestamp_file):
        with open(timestamp_file, "w") as f:
            f.write(str(time.time()))
    else:
        with open(timestamp_file, "r+") as f:
            f.write(str(time.time()))

def is_obsidian_uri(uri: str) -> bool:
    return uri.startswith("obsidian://")

def get_obsidian_file_path(uri: str) -> str:
    return uri.replace("obsidian://", "")