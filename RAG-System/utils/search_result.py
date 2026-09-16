from dataclasses import dataclass
from typing import Any

from utils.chunk import Chunk


@dataclass
class SearchResult:
    score: float
    chunk: Chunk
    document_id: int | None = None

    def __getitem__(self, key: str) -> Any:
        if key == "score":
            return self.score
        if key == "chunk":
            return self.chunk
        if key == "document_id":
            return self.document_id
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default