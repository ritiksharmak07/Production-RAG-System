from preprocessing.cleaner import TextCleaner
from preprocessing.metadata_extractor import MetadataExtractor


class PreprocessingPipeline:

    def process(self, documents):

        processed_documents = []

        for document in documents:

            document.text = TextCleaner.clean(document.text)

            document = MetadataExtractor.enrich(document)

            processed_documents.append(document)

        return processed_documents