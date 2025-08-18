import logging
from pathlib import Path

from indexer.domain.repositories.anime_repository import AnimeRepository
from indexer.domain.repositories.csv_data_source import CsvDataSource
from indexer.domain.services.anime_indexing_service import AnimeIndexingService


class IndexAnimeDataUseCase:
    """Application use case for indexing anime data from CSV."""
    
    def __init__(
        self,
        anime_repository: AnimeRepository,
        csv_data_source: CsvDataSource,
        anime_indexing_service: AnimeIndexingService
    ):
        self.anime_repository = anime_repository
        self.csv_data_source = csv_data_source
        self.anime_indexing_service = anime_indexing_service
        self.logger = logging.getLogger(__name__)
    
    def execute(self, csv_file_path: str) -> bool:
        """
        Execute the anime data indexing use case.
        
        Args:
            csv_file_path: Path to the CSV file containing anime data
            
        Returns:
            True if indexing was successful, False otherwise
        """
        
        try:
            self.logger.info("Starting anime data indexing process")
            
            # Validate input
            if not csv_file_path or not Path(csv_file_path).exists():
                self.logger.error(f"CSV file not found: {csv_file_path}")
                return False
            
            # Ensure index exists
            if not self.anime_indexing_service.ensure_index_exists():
                self.logger.error("Failed to ensure index exists")
                return False
            
            # Read anime data from CSV
            self.logger.info("Reading anime data from CSV file")
            animes = self.csv_data_source.read_anime_data(csv_file_path)
            
            if not animes:
                self.logger.warning("No anime data found in CSV file")
                return False
            
            self.logger.info(f"Successfully read {len(animes)} anime records")
            
            # Index the anime data
            self.logger.info("Starting anime data indexing")
            success_count, failed_count = self.anime_indexing_service.index_anime_batch(animes)
            
            total_records = len(animes)
            success_rate = (success_count / total_records) * 100 if total_records > 0 else 0
            
            self.logger.info(
                f"Indexing completed: {success_count}/{total_records} successful "
                f"({success_rate:.1f}% success rate), {failed_count} failed"
            )
            
            # Consider the operation successful if at least 90% of records were indexed
            return success_rate >= 90.0
            
        except Exception as e:
            self.logger.error(f"Error during anime data indexing: {e}")
            return False
