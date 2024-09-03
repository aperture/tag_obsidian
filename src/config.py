import logging
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    open_ai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings: Settings = Settings()

# Directory containing your Obsidian notes
# This is the directory where the script will look for .md files to process
obsidian_notes_dir: str = "/Users/adamhaslip/Library/Mobile Documents/iCloud~md~obsidian/Documents/Adams Managed Vault"
excluded_dirs: List[str] = [
    "attachments", ".obsidian", ".trash", "🛠️ ~workspace", "🗄️~archive"
]

# File to store and maintain the list of tags
tags_file: str = "tags.txt"
timestamp_file: str = "last_run_timestamp.txt"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
