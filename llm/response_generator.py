import logging
from llm.gemini_client import GeminiClient
from llm.prompt_builder import PromptBuilder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LLMServiceUnavailableError(Exception):
    """Custom exception for when the LLM service is not available."""
    pass

class ResponseGenerator:

    def __init__(self):

        try:
            self.llm = GeminiClient()
        except Exception as exc:
            print(f"Gemini client unavailable: {exc}")
            logging.error(f"Gemini client unavailable: {exc}", exc_info=True)
            self.llm = None

    def generate(

        self,

        query,

        search_results

    ):

        prompt = PromptBuilder().build(

            query,

            search_results

        )

        if self.llm is None:
            return (
                "Response generation is unavailable because the local LLM backend "
                "is not running."
            )
            raise LLMServiceUnavailableError("LLM client is not initialized. Cannot generate response.")

        answer = self.llm.generate(

            prompt

        )

        return answer