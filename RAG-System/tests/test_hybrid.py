from embeddings.embedding_generator import EmbeddingGenerator
from retriever.hybrid_search import HybridRetriever
from utils.chunk import Chunk
from vector_store.index_manager import FAISSIndexManager

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
        text="EAR formula is used in drowsiness detection.",
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
    embeddings.shape[1]
)

manager.add_embeddings(
    embeddings,
    chunks
)

retriever = HybridRetriever(
    manager,
    chunks
)

results = retriever.retrieve(
    "Explain EAR formula",
    top_k=3
)

for result in results:

    print("=" * 50)

    print(result.score)

    print(result.chunk.text)