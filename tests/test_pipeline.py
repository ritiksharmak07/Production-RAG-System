from utils.chunk import Chunk

from embeddings.embedding_generator import EmbeddingGenerator

from vector_store.index_manager import FAISSIndexManager

from pipeline.rag_pipeline import RAGPipeline


chunks = [

    Chunk(
        text="Python is a programming language.",
        metadata={}
    ),

    Chunk(
        text="Python is widely used in Artificial Intelligence.",
        metadata={}
    ),

    Chunk(
        text="Machine Learning uses Python extensively.",
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

pipeline = RAGPipeline(
    manager,
    chunks
)

response = pipeline.ask(
    "What is Python used for?"
)

print(response["answer"])

print()

print("Sources")

for source in response["sources"]:

    print("-"*50)

    print(source.score)

    print(source.chunk.text)