"""Dependency injection container for the anime indexer application."""

import logging
from elasticsearch import Elasticsearch

from indexer.infrastructure.config import parse_args
from indexer.infrastructure.logging.logger_config import setup_application_logging
from indexer.infrastructure.repositories.elasticsearch_anime_repository import ElasticsearchAnimeRepository
from indexer.infrastructure.data_sources.anime_csv_data_source import AnimeCsvDataSource
from indexer.domain.services.anime_indexing_service import AnimeIndexingService
from indexer.application.use_cases.index_anime_data_use_case import IndexAnimeDataUseCase


class Container:
    """Dependency injection container."""
    
    def __init__(self, log_level: str = "INFO", log_file: str = None):
        self.logger = setup_application_logging(log_level, log_file)
        self.args = parse_args()
        
        # Infrastructure
        self._elasticsearch_client = None
        self._anime_repository = None
        self._csv_data_source = None
        
        # Domain services
        self._anime_indexing_service = None
        
        # Application use cases
        self._index_anime_data_use_case = None
    
    @property
    def elasticsearch_client(self) -> Elasticsearch:
        """Get the Elasticsearch client instance."""
        if not self._elasticsearch_client:
            self.logger.info("Creating Elasticsearch client")
            
            self._elasticsearch_client = Elasticsearch(
                hosts=[{
                    "host": self.args.elasticsearch_host,
                    "port": self.args.elasticsearch_port,
                    "scheme": "http"
                }],
                request_timeout=60,
                retry_on_timeout=True,
                max_retries=3
            )
            
            # Test connection
            try:
                client_info = self._elasticsearch_client.info()
                self.logger.info("Successfully connected to Elasticsearch")
                self.logger.debug(f"Elasticsearch info: {client_info}")
            except Exception as e:
                self.logger.error(f"Failed to connect to Elasticsearch: {e}")
                raise
        
        return self._elasticsearch_client
    
    @property
    def anime_repository(self) -> ElasticsearchAnimeRepository:
        """Get the anime repository instance."""
        if not self._anime_repository:
            self._anime_repository = ElasticsearchAnimeRepository(self.elasticsearch_client)
        return self._anime_repository
    
    @property
    def csv_data_source(self) -> AnimeCsvDataSource:
        """Get the CSV data source instance."""
        if not self._csv_data_source:
            self._csv_data_source = AnimeCsvDataSource()
        return self._csv_data_source
    
    @property
    def anime_indexing_service(self) -> AnimeIndexingService:
        """Get the anime indexing service instance."""
        if not self._anime_indexing_service:
            self._anime_indexing_service = AnimeIndexingService(self.anime_repository)
        return self._anime_indexing_service
    
    @property
    def index_anime_data_use_case(self) -> IndexAnimeDataUseCase:
        """Get the index anime data use case instance."""
        if not self._index_anime_data_use_case:
            self._index_anime_data_use_case = IndexAnimeDataUseCase(
                self.anime_repository,
                self.csv_data_source,
                self.anime_indexing_service
            )
        return self._index_anime_data_use_case
