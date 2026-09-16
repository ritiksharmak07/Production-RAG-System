import numpy as np


class EmbeddingCache:

    @staticmethod
    def save(path, embeddings):

        np.save(path, embeddings)

    @staticmethod
    def load(path):

        return np.load(path)