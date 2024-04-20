from pathlib import Path
from dataclasses import dataclass
import os



@dataclass(frozen=True)
class GithubUrlIngestionConfig:
    """
        Represents the configuration for ingesting data from a GitHub URL.

        Attributes:
            github_dir (Path): The directory where the GitHub data will be ingested.
    """
    github_dir: Path


@dataclass(frozen=True)
class StoreEmbeddingVectorDBConfig:
    """
        Represents the configuration for storing embedding vectors in a database.

        Fields:
        - chunk_size: An integer representing the size of each chunk of embedding vectors.
        - overlap: An integer representing the overlap between consecutive chunks.
        - embedding_model_name: A string representing the name of the embedding model.
        - github_dir: A Path object representing the directory where the GitHub data is stored.
        - chromadb_dir: A Path object representing the directory where the ChromaDB data is stored.
    """
    chunk_zise: int
    overlap: int
    embedding_model_name: str
    github_dir: Path
    chromadb_dir: Path