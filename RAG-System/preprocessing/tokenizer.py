class Tokenizer:

    @staticmethod
    def word_count(text: str):

        return len(text.split())

    @staticmethod
    def character_count(text: str):

        return len(text)

    @staticmethod
    def sentence_count(text: str):

        return len(
            [s for s in text.split(".") if s.strip()]
        )