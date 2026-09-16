from utils.chunk import Chunk

from embeddings.embedding_generator import EmbeddingGenerator

from vector_store.index_manager import FAISSIndexManager

from retriever.retriever import Retriever


chunks = [

    Chunk(

        text="Python is a programming language.",

        metadata={"id":1}

    ),

    Chunk(

        text="Machine Learning uses Python.",

        metadata={"id":2}

    ),

    Chunk(

        text="The sky is blue.",

        metadata={"id":3}

    ),

    Chunk(

        text="Deep Learning is a subset of Machine Learning.",

        metadata={"id":4}

    )

]

generator = EmbeddingGenerator()

embeddings = generator.generate_chunks(chunks)

faiss_manager = FAISSIndexManager(

    embeddings.shape[1]

)

faiss_manager.add_embeddings(

    embeddings,

    chunks

)

retriever = Retriever(

    faiss_manager

)

results = retriever.retrieve(

    "What is Python?",

    top_k=3

)

for result in results:

    print("="*60)

    print("Similarity:", result["score"])

    print(result["chunk"].text)