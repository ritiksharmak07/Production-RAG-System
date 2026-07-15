from dataclasses import dataclass
from utils.chunk import Chunk


@dataclass
class SearchResult:
    score: float
    chunk: Chunk
    document_id: int