from abc import ABC, abstractmethod
from typing import List, Optional
from indexer.domain.entities.anime import Anime


class AnimeRepository(ABC):
    """Abstract repository interface for Anime operations."""
    
    @abstractmethod
    def create_index(self) -> bool:
        """Create the anime index with proper mappings."""
        pass
    
    @abstractmethod
    def index_exists(self) -> bool:
        """Check if the anime index exists."""
        pass
    
    @abstractmethod
    def bulk_index(self, animes: List[Anime]) -> tuple[int, int]:
        """
        Bulk index a list of anime entities.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        pass
    
    @abstractmethod
    def index_anime(self, anime: Anime) -> bool:
        """Index a single anime entity."""
        pass
    
    @abstractmethod
    def get_anime_by_id(self, anime_id: int) -> Optional[Anime]:
        """Retrieve an anime by its ID."""
        pass
    
    @abstractmethod
    def search_anime(self, query: str, limit: int = 10) -> List[Anime]:
        """Search for anime based on a query."""
        pass
    
    @abstractmethod
    def delete_index(self) -> bool:
        """Delete the anime index."""
        pass
