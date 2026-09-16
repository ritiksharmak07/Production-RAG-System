import os
from pathlib import Path

from dotenv import load_dotenv

from configs.model_config import LLM_MODEL

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

try:
    from google import genai as google_genai
except ImportError:
    google_genai = None

try:
    import google.generativeai as generativeai
except ImportError:
    generativeai = None


class GeminiClient:
    """Gemini API client for text generation."""

    def __init__(
        self,
        model_name: str = LLM_MODEL,
        api_key: str | None = None,
    ):
        self.model_name = model_name or LLM_MODEL
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.available = bool(self.api_key)
        self.backend = None
        self.client = None
        self.model = None

        if not self.api_key:
            return

        if google_genai is not None:
            self.client = google_genai.Client(api_key=self.api_key)
            self.backend = "google-genai"
            self.model = self.model_name
            return

        if generativeai is not None:
            generativeai.configure(api_key=self.api_key)
            self.backend = "google-generativeai"
            self.model = generativeai.GenerativeModel(self.model_name)
            return

        self.available = False

    def _fallback_model(self):
        candidates = [
            "gemini-3.6-flash",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            self.model_name,
        ]
        seen = set()
        for candidate in candidates:
            if candidate and candidate not in seen:
                seen.add(candidate)
                self.model_name = candidate
                if self.backend == "google-genai":
                    self.model = candidate
                    return
                if self.backend == "google-generativeai":
                    self.model = generativeai.GenerativeModel(candidate)
                    return

    def _generate_with_backend(self, prompt: str, max_tokens: int, temperature: float):
        if self.backend == "google-genai":
            return self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )

        return self.model.generate_content(
            contents=prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

    def _extract_text(self, response: object) -> str:
        if hasattr(response, "text") and response.text:
            return response.text

        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                for part in getattr(candidate, "content", []).parts:
                    if getattr(part, "text", None):
                        return part.text

        raise RuntimeError("Unable to read Gemini response text.")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """Generate a response using Gemini."""
        if not self.available:
            return "LLM backend is not configured. Set GEMINI_API_KEY to enable answer generation."

        try:
            response = self._generate_with_backend(prompt, max_tokens, temperature)
            return self._extract_text(response)
        except Exception as exc:
            message = str(exc)
            if "NOT_FOUND" in message or "is not found" in message or "no longer available" in message:
                self._fallback_model()
                try:
                    response = self._generate_with_backend(prompt, max_tokens, temperature)
                    return self._extract_text(response)
                except Exception as fallback_exc:
                    return f"LLM backend is unavailable right now: {fallback_exc}"
            return f"LLM backend is unavailable right now: {exc}"

    def chat(
        self,
        messages: list[dict],
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """Simple chat wrapper."""
        if not self.available:
            return "LLM backend is not configured. Set GEMINI_API_KEY to enable chat generation."

        if self.backend == "google-genai":
            contents = []
            for message in messages:
                contents.append({"role": message["role"], "parts": [{"text": message["content"]}]})
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return self._extract_text(response)

        history = [
            {"role": message["role"], "parts": [message["content"]]}
            for message in messages
        ]
        *chat_history, current_prompt = history
        chat = self.model.start_chat(history=chat_history)
        response = chat.send_message(
            content=current_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        return self._extract_text(response)