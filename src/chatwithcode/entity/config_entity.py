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