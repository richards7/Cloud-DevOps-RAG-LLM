import google.generativeai as genai
from app.llm.base import LLMProvider
from app.config import settings


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
