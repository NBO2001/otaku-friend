import logging
from typing import List
from indexer.domain.entities.anime import Anime
from indexer.domain.repositories.anime_repository import AnimeRepository


class AnimeIndexingService:
    """Domain service for anime indexing business logic."""
    
    def __init__(self, anime_repository: AnimeRepository):
        self.anime_repository = anime_repository
        self.logger = logging.getLogger(__name__)
    
    def ensure_index_exists(self) -> bool:
        """Ensure the anime index exists, create it if not."""
        try:
            if not self.anime_repository.index_exists():
                self.logger.info("Anime index does not exist, creating...")
                success = self.anime_repository.create_index()
                if success:
                    self.logger.info("Anime index created successfully")
                else:
                    self.logger.error("Failed to create anime index")
                return success
            else:
                self.logger.info("Anime index already exists")
                return True
        except Exception as e:
            self.logger.error(f"Error checking/creating index: {e}")
            return False
    
    def index_anime_batch(self, animes: List[Anime]) -> tuple[int, int]:
        """
        Index a batch of anime entities with business logic validation.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        if not animes:
            self.logger.warning("No anime data provided for indexing")
            return 0, 0
        
        self.logger.info(f"Starting bulk indexing of {len(animes)} anime records")
        
        # Validate all entities before indexing
        valid_animes = []
        invalid_count = 0
        
        for anime in animes:
            try:
                # The entity validation happens in __post_init__
                valid_animes.append(anime)
            except ValueError as e:
                self.logger.warning(f"Invalid anime data for ID {getattr(anime, 'anime_id', 'unknown')}: {e}")
                invalid_count += 1
        
        if invalid_count > 0:
            self.logger.warning(f"Skipped {invalid_count} invalid anime records")
        
        if not valid_animes:
            self.logger.error("No valid anime records to index")
            return 0, len(animes)
        
        try:
            success_count, failed_count = self.anime_repository.bulk_index(valid_animes)
            
            self.logger.info(f"Indexing completed: {success_count} successful, {failed_count} failed")
            
            if failed_count > 0:
                self.logger.warning(f"{failed_count} records failed to index")
            
            return success_count, failed_count + invalid_count
            
        except Exception as e:
            self.logger.error(f"Error during bulk indexing: {e}")
            return 0, len(animes)
    
    def validate_anime_data(self, anime: Anime) -> bool:
        """Validate anime entity according to business rules."""
        try:
            # Business validation rules
            if not anime.title or not anime.title.strip():
                return False
            
            if anime.anime_id <= 0:
                return False
            
            if anime.score < 0 or anime.score > 10:
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Validation error for anime {anime.anime_id}: {e}")
            return False
