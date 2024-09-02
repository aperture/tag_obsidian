from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.open_ai_api_key)