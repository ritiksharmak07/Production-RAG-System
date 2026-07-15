from embeddings.embedding_generator import EmbeddingGenerator
from utils.chunk import Chunk

chunks = [
    Chunk(
        text="Python is a programming language.",
        metadata={}
    ),
    Chunk(
        text="Machine Learning uses Python.",
        metadata={}
    ),
    Chunk(
        text="The sky is blue.",
        metadata={}
    )
]

generator = EmbeddingGenerator()

embeddings = generator.generate_chunks(chunks)

print("\nEmbedding Shape:")
print(embeddings.shape)

print("\nFirst Embedding:")
print(embeddings[0])

query_embedding = generator.generate_query_embedding(
    "What is Python?"
)

print("\nQuery Shape:")
print(query_embedding.shape)