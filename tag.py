import os
from openai import OpenAI
import argparse
import time
from pydantic_settings import BaseSettings

# Set up your OpenAI API key
class Settings(BaseSettings):
    open_ai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
client = OpenAI(api_key=settings.open_ai_api_key)

# Directory containing your Obsidian notes
obsidian_notes_dir = "/Users/adamhaslip/Library/Mobile Documents/iCloud~md~obsidian/Documents/Adams Managed Vault"
exluded_dirs = [
    "attachments", ".obsidian", ".trash", "🛠️ ~workspace", "🗄️~archive"
]

# File to store and maintain the list of tags
tags_file = "tags.txt"
timestamp_file = "last_run_timestamp.txt"

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

def generate_tags(content, existing_tags):
    existing_tags_str = " ".join(existing_tags)

    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that generates relevant tags for content, ensuring consistency with existing tags."
        },
        {
            "role": "user",
            "content": f"Here are the existing tags: {existing_tags_str}. Please generate relevant hashtags for the following content:\n\n{content}, return each tag on a new line starting with a #"
        }
    ])

    generated_tags = response.choices[0].message.content.splitlines()
    tags = {line.strip() for line in generated_tags if line.startswith("#")}

    return tags


def dry_run_generate_tag_list(directory, specific_file=None):
    all_tags = load_existing_tags()
    last_run_timestamp = load_last_run_timestamp()
    
    if specific_file:
        files_to_process = [specific_file]
    else:
        files_to_process = []
        for root, _, files in os.walk(directory):
            if any(excluded_dir in root for excluded_dir in exluded_dirs):
                continue
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    if os.path.getmtime(filepath) > last_run_timestamp:
                        files_to_process.append(filepath)
    
    for filepath in files_to_process:
        with open(filepath, "r") as file_content:
            content = file_content.read()
            tags = generate_tags(content, all_tags)
            all_tags.update(tags)
            save_tags(all_tags)

    save_current_timestamp()
    print("Dry run complete! Tag list generated and saved.")

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
