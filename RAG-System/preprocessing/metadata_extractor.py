from preprocessing.tokenizer import Tokenizer

class MetadataExtractor:

    @staticmethod
    def enrich(document):

        document.metadata["word_count"] = \
            Tokenizer.word_count(document.text)

        document.metadata["character_count"] = \
            Tokenizer.character_count(document.text)

        document.metadata["sentence_count"] = \
            Tokenizer.sentence_count(document.text)

        return document