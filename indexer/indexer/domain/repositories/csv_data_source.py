from abc import ABC, abstractmethod
from typing import List
from indexer.domain.entities.anime import Anime


class CsvDataSource(ABC):
    """Abstract interface for CSV data source operations."""
    
    @abstractmethod
    def read_anime_data(self, file_path: str) -> List[Anime]:
        """Read anime data from CSV file and return list of Anime entities."""
        pass
