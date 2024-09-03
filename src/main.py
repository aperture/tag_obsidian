import argparse
from config import settings, obsidian_notes_dir
from tag_generator import update_tag_list
from typing import Optional
from config import logger

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate tag list for Obsidian notes.")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Specific file to process"
    )
    return parser.parse_args()

if __name__ == "__main__":
    logger.info("Starting tag generation process...")
    args: argparse.Namespace = parse_args()
    if True:
        update_tag_list(obsidian_notes_dir, args.file)
