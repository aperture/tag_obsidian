from openai import OpenAI
from config import settings
from typing import List, Set

client = OpenAI(api_key=settings.open_ai_api_key)

class OpenAIClient:
    def __init__(self) -> None:
        self.client: OpenAI = OpenAI(api_key=settings.open_ai_api_key)

    def get_relevant_tags(self, content: str, existing_tags: Set[str]) -> Set[str]:
        existing_tags_str: str = " ".join(existing_tags)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates relevant tags for content, ensuring consistency with existing tags."
                },
                {
                    "role": "user",
                    "content": f"Existing tags: {existing_tags_str}\nContent: {content}"
                }
            ]
        )
        return set(response.choices[0].message.content.split())

openai_client: OpenAIClient = OpenAIClient()
