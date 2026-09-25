"""
Tries each configured LLM provider in order and falls back to the
next one if a call fails (timeout, rate limit, invalid key, etc).
This is the "connecting APIs of different LLMs" piece of the project.
"""
import logging
from app.llm.gemini_provider import GeminiProvider
from app.config import settings

logger = logging.getLogger(__name__)


class LLMRouter:
    def __init__(self):
        self.providers = []

        if settings.GEMINI_API_KEY:
            self.providers.append(GeminiProvider())

        if not self.providers:
            raise ValueError(
                "No LLM providers configured. Set GEMINI_API_KEY "
                "in your .env file."
            )

    def generate(self, prompt: str) -> dict:
        last_error = None
        for provider in self.providers:
            try:
                text = provider.generate(prompt)
                return {"text": text, "provider": provider.name}
            except Exception as e:
                logger.warning("Provider %s failed: %s", provider.name, e)
                last_error = e
                continue
        raise RuntimeError(f"All LLM providers failed. Last error: {last_error}")


_router = None


def get_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
