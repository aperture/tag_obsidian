import os
from config import excluded_dirs
from openai_client import client
from utils import load_existing_tags, load_last_run_timestamp, save_current_timestamp, save_tags

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
            if any(exclude_dir in root for exclude_dir in excluded_dirs):
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