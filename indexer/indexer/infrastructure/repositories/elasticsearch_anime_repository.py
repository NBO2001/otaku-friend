import logging
from typing import List, Optional
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from indexer.domain.entities.anime import Anime
from indexer.domain.repositories.anime_repository import AnimeRepository


class ElasticsearchAnimeRepository(AnimeRepository):
    """Elasticsearch implementation of the AnimeRepository."""
    
    INDEX_NAME = "anime"
    
    def __init__(self, elasticsearch_client: Elasticsearch):
        self.es = elasticsearch_client
        self.logger = logging.getLogger(__name__)
    
    def create_index(self) -> bool:
        """Create the anime index with proper mappings."""
        try:
            settings = self._get_index_settings()
            self.es.indices.create(index=self.INDEX_NAME, body=settings)
            self.logger.info(f"Index '{self.INDEX_NAME}' created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error creating index '{self.INDEX_NAME}': {e}")
            return False
    
    def index_exists(self) -> bool:
        """Check if the anime index exists."""
        try:
            return self.es.indices.exists(index=self.INDEX_NAME)
        except Exception as e:
            self.logger.error(f"Error checking if index exists: {e}")
            return False
    
    def bulk_index(self, animes: List[Anime]) -> tuple[int, int]:
        """
        Bulk index a list of anime entities.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        def doc_generator():
            for i, anime in enumerate(animes):
                yield {
                    "_index": self.INDEX_NAME,
                    "_id": anime.anime_id,
                    "_source": anime.to_elasticsearch_doc()
                }
        
        try:
            success_count, failed_docs = bulk(
                self.es,
                doc_generator(),
                chunk_size=500,
                request_timeout=60,
                max_retries=3,
                initial_backoff=2,
                max_backoff=600
            )
            
            failed_count = len(failed_docs) if failed_docs else 0
            
            self.logger.info(f"Bulk indexing completed: {success_count} successful, {failed_count} failed")
            
            if failed_docs:
                for failed_doc in failed_docs[:5]:  # Log first 5 failures
                    self.logger.warning(f"Failed to index document: {failed_doc}")
            
            return success_count, failed_count
            
        except Exception as e:
            self.logger.error(f"Error during bulk indexing: {e}")
            # Fall back to individual indexing
            return self._fallback_individual_indexing(animes)
    
    def index_anime(self, anime: Anime) -> bool:
        """Index a single anime entity."""
        try:
            self.es.index(
                index=self.INDEX_NAME,
                id=anime.anime_id,
                document=anime.to_elasticsearch_doc()
            )
            self.logger.debug(f"Successfully indexed anime {anime.anime_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error indexing anime {anime.anime_id}: {e}")
            return False
    
    def get_anime_by_id(self, anime_id: int) -> Optional[Anime]:
        """Retrieve an anime by its ID."""
        try:
            response = self.es.get(index=self.INDEX_NAME, id=anime_id)
            source = response['_source']
            
            # Convert back to Anime entity
            return self._dict_to_anime(source)
            
        except Exception as e:
            self.logger.error(f"Error retrieving anime {anime_id}: {e}")
            return None
    
    def search_anime(self, query: str, limit: int = 10) -> List[Anime]:
        """Search for anime based on a query."""
        try:
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "synopsis", "genres"]
                    }
                },
                "size": limit
            }
            
            response = self.es.search(index=self.INDEX_NAME, body=search_body)
            
            animes = []
            for hit in response['hits']['hits']:
                anime = self._dict_to_anime(hit['_source'])
                if anime:
                    animes.append(anime)
            
            return animes
            
        except Exception as e:
            self.logger.error(f"Error searching anime: {e}")
            return []
    
    def delete_index(self) -> bool:
        """Delete the anime index."""
        try:
            self.es.indices.delete(index=self.INDEX_NAME)
            self.logger.info(f"Index '{self.INDEX_NAME}' deleted successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting index '{self.INDEX_NAME}': {e}")
            return False
    
    def _get_index_settings(self) -> dict:
        """Get the index settings and mappings for anime data."""
        return {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "gen_analyzer": {
                            "tokenizer": "keyword",
                            "filter": ["word_delimiter", "lowercase"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "anime_id": {"type": "integer"},
                    "anime_url": {"type": "keyword"},
                    "title": {"type": "text"},
                    "synopsis": {"type": "text"},
                    "main_pic": {"type": "keyword"},
                    "type": {"type": "keyword"},
                    "source_type": {"type": "keyword"},
                    "num_episodes": {"type": "rank_feature"},
                    "status": {"type": "keyword"},
                    "start_date": {"type": "date"},
                    "end_date": {"type": "date"},
                    "season": {"type": "keyword"},
                    "studios": {"type": "keyword"},
                    "genres": {
                        "type": "text",
                        "analyzer": "gen_analyzer"
                    },
                    "score": {"type": "rank_feature"},
                    "score_count": {"type": "rank_feature"},
                    "score_rank": {"type": "integer"},
                    "popularity_rank": {"type": "integer"},
                    "members_count": {"type": "integer"},
                    "favorites_count": {"type": "integer"},
                    "watching_count": {"type": "integer"},
                    "completed_count": {"type": "rank_feature"},
                    "on_hold_count": {"type": "integer"},
                    "dropped_count": {
                        "type": "rank_feature",
                        "positive_score_impact": False
                    },
                    "plan_to_watch_count": {"type": "integer"},
                    "total_count": {"type": "integer"},
                    "score_10_count": {"type": "integer"},
                    "score_09_count": {"type": "integer"},
                    "score_08_count": {"type": "integer"},
                    "score_07_count": {"type": "integer"},
                    "score_06_count": {"type": "integer"},
                    "score_05_count": {"type": "integer"},
                    "score_04_count": {"type": "integer"},
                    "score_03_count": {"type": "integer"},
                    "score_02_count": {"type": "integer"},
                    "score_01_count": {"type": "integer"},
                    "clubs": {"type": "keyword"},
                    "pics": {"type": "keyword"}
                }
            }
        }
    
    def _fallback_individual_indexing(self, animes: List[Anime]) -> tuple[int, int]:
        """Fallback to individual indexing when bulk fails."""
        self.logger.info("Falling back to individual document indexing...")
        
        success_count = 0
        failed_count = 0
        
        for anime in animes:
            if self.index_anime(anime):
                success_count += 1
            else:
                failed_count += 1
            
            if (success_count + failed_count) % 100 == 0:
                self.logger.info(f"Processed {success_count + failed_count} documents...")
        
        self.logger.info(f"Individual indexing completed: {success_count} successful, {failed_count} failed")
        return success_count, failed_count
    
    def _dict_to_anime(self, data: dict) -> Optional[Anime]:
        """Convert dictionary data back to Anime entity."""
        try:
            # Handle date parsing
            from datetime import datetime
            
            start_date = None
            if data.get('start_date'):
                start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            
            end_date = None
            if data.get('end_date'):
                end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
            
            return Anime(
                anime_id=data['anime_id'],
                title=data['title'],
                synopsis=data['synopsis'],
                anime_url=data.get('anime_url'),
                main_pic=data.get('main_pic'),
                type=data.get('type'),
                source_type=data.get('source_type'),
                num_episodes=data.get('num_episodes', 1),
                status=data.get('status'),
                start_date=start_date,
                end_date=end_date,
                season=data.get('season'),
                studios=data.get('studios'),
                genres=data.get('genres'),
                score=data.get('score', 0.1),
                score_count=data.get('score_count', 1),
                score_rank=data.get('score_rank', 0),
                popularity_rank=data.get('popularity_rank', 0),
                members_count=data.get('members_count', 0),
                favorites_count=data.get('favorites_count', 0),
                watching_count=data.get('watching_count', 0),
                completed_count=data.get('completed_count', 1),
                on_hold_count=data.get('on_hold_count', 0),
                dropped_count=data.get('dropped_count', 1),
                plan_to_watch_count=data.get('plan_to_watch_count', 0),
                total_count=data.get('total_count', 0),
                score_10_count=data.get('score_10_count', 0),
                score_09_count=data.get('score_09_count', 0),
                score_08_count=data.get('score_08_count', 0),
                score_07_count=data.get('score_07_count', 0),
                score_06_count=data.get('score_06_count', 0),
                score_05_count=data.get('score_05_count', 0),
                score_04_count=data.get('score_04_count', 0),
                score_03_count=data.get('score_03_count', 0),
                score_02_count=data.get('score_02_count', 0),
                score_01_count=data.get('score_01_count', 0),
                clubs=data.get('clubs'),
                pics=data.get('pics')
            )
        except Exception as e:
            self.logger.error(f"Error converting dict to Anime: {e}")
            return None
