import os
from typing import Optional, List, Set
from config import excluded_dirs, logger
from openai_client import openai_client
from file_utils import get_existing_tags, get_last_run_timestamp, update_timestamp, save_tags, get_obsidian_file_path, is_obsidian_uri

def update_tag_list(directory: str, specific_file: Optional[str] = None) -> None:
    all_tags: Set[str] = get_existing_tags()
    logger.info(f"Existing tags: {all_tags}")
    last_run_timestamp: float = get_last_run_timestamp()
    
    if specific_file:
        if is_obsidian_uri(specific_file):
            specific_file = get_obsidian_file_path(specific_file)
        files_to_process: List[str] = [specific_file]
    else:
        files_to_process: List[str] = []
        for root, _, files in os.walk(directory):
            if any(exclude_dir in root for exclude_dir in excluded_dirs):
                continue
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    logger.info(f"Checking file: {filepath}")
                    if os.path.getmtime(filepath) > last_run_timestamp:
                        files_to_process.append(filepath)
    
    for filepath in files_to_process:
        with open(filepath, "r") as file_content:
            content = file_content.read()
            tags = openai_client.get_relevant_tags(content, all_tags)
            all_tags.update(tags)
            save_tags(all_tags)

    update_timestamp()
    logger.info("Dry run complete! Tag list generated and saved.")

