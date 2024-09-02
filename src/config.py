from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    open_ai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Directory containing your Obsidian notes
obsidian_notes_dir = "/Users/adamhaslip/Library/Mobile Documents/iCloud~md~obsidian/Documents/Adams Managed Vault"
excluded_dirs = [
    "attachments", ".obsidian", ".trash", "🛠️ ~workspace", "🗄️~archive"
]

# File to store and maintain the list of tags
tags_file = "tags.txt"
timestamp_file = "last_run_timestamp.txt"