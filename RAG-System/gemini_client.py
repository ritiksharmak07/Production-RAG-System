from __future__ import annotations

import os
from typing import Any, Dict

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GeminiClient:
    """Client for Google Gemini model inference."""

    def __init__(self, model_name: str = "gemini-1.5-flash-latest", api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        """
        Generates a response from the Gemini model.
        """
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

        try:
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            # Broad exception for simplicity, can be refined to handle specific API errors
            raise RuntimeError(f"Gemini API request failed: {e}") from e

    def chat(self, messages: list[Dict[str, Any]], max_tokens: int = 512, temperature: float = 0.2) -> str:
        """
        A simple chat implementation.
        """
        # The Gemini API prefers a structured chat history.
        # For this simple implementation, we'll just concatenate the messages.
        # For a more advanced use case, you would pass a list of `glm.Content` objects.
        prompt = "\n".join(f"{message['role'].capitalize()}: {message['content']}" for message in messages)
        return self.generate(prompt=prompt, max_tokens=max_tokens, temperature=temperature)