"""
Abstract interface every LLM provider must implement. This is what
lets the router treat Gemini, OpenAI (or any future provider)
interchangeably — a direct application of the abstraction pillar
of OOP.
"""
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name = "base"

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Send the prompt to the provider and return the text response."""
        raise NotImplementedError
