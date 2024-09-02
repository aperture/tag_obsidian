import argparse
from config import settings, obsidian_notes_dir
from tag_generator import dry_run_generate_tag_list

def parse_args():
    parser = argparse.ArgumentParser(description="Generate tag list for Obsidian notes.")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Specific file to process"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    dry_run_generate_tag_list(obsidian_notes_dir, args.file)