from embeddings.embedding_generator import EmbeddingGenerator
from vector_store.index_manager import FAISSIndexManager
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

embeddings = generator.generate_chunks(
    chunks
)

manager = FAISSIndexManager(
    embedding_dimension=embeddings.shape[1]
)

manager.add_embeddings(
    embeddings,
    chunks
)

query = generator.generate_query_embedding(
    "Tell me about Python"
)

results = manager.search(
    query,
    top_k=2
)

for result in results:

    print("="*60)

    print("Similarity:", result["score"])

    print(result["chunk"].text)