import os

from google import genai
from google.generativeai import types

from configs.model_config import LLM_MODEL


class GeminiClient:
    """
    Gemini API client for text generation.
    """

    def __init__(
        self,
        model_name: str = LLM_MODEL,
        api_key: str | None = None,
    ):

        self.model_name = model_name

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate a response using Gemini.
        """

        try:

            generation_config = types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
            )
            response = self.model.generate_content(
                contents=prompt,
                generation_config=generation_config,
            )

            return response.text

        except Exception as exc:
            raise RuntimeError(
                f"Gemini generation failed: {exc}"
            ) from exc

    def chat(
        self,
        messages: list[dict],
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """
        Simple chat wrapper.
        """

        # The new google-genai SDK prefers a different message format.
        # The old format was: `{'role': 'user', 'content': '...'}`
        # The new format is: `{'role': 'user', 'parts': ['...']}`
        history = [
            {"role": message["role"], "parts": [message["content"]]}
            for message in messages
        ]

        # The last message is the new prompt
        *chat_history, current_prompt = history
        chat = self.model.start_chat(history=chat_history)
        response = chat.send_message(current_prompt)
        generation_config = types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
        )
        response = chat.send_message(
            content=current_prompt, generation_config=generation_config
        )
        return response.text