from llm.prompt_template import SYSTEM_PROMPT

class PromptBuilder:
    """Build a prompt for the LLM from the query and context."""

    def __init__(self):
        pass

    def build(self, query, search_results):
    @staticmethod
    def build(query: str, search_results: list) -> str:
        context = "\n\n".join(
            f"Source {index + 1}: {result.chunk.text}"
            for index, result in enumerate(search_results)
        )

        return f"""{SYSTEM_PROMPT}

Question: {query}

Context:
{context}
"""
