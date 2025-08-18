from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Anime:
    """Anime domain entity representing the core anime data structure."""
    
    anime_id: int
    title: str
    synopsis: str
    anime_url: Optional[str] = None
    main_pic: Optional[str] = None
    type: Optional[str] = None
    source_type: Optional[str] = None
    num_episodes: int = 1
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    season: Optional[str] = None
    studios: Optional[str] = None
    genres: Optional[str] = None
    score: float = 0.1
    score_count: int = 1
    score_rank: int = 0
    popularity_rank: int = 0
    members_count: int = 0
    favorites_count: int = 0
    watching_count: int = 0
    completed_count: int = 1
    on_hold_count: int = 0
    dropped_count: int = 1
    plan_to_watch_count: int = 0
    total_count: int = 0
    score_10_count: int = 0
    score_09_count: int = 0
    score_08_count: int = 0
    score_07_count: int = 0
    score_06_count: int = 0
    score_05_count: int = 0
    score_04_count: int = 0
    score_03_count: int = 0
    score_02_count: int = 0
    score_01_count: int = 0
    clubs: Optional[str] = None
    pics: Optional[str] = None

    def __post_init__(self):
        """Validate business rules after initialization."""
        if self.anime_id <= 0:
            raise ValueError("Anime ID must be positive")
        
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        
        if self.score < 0 or self.score > 10:
            raise ValueError("Score must be between 0 and 10")
        
        # Ensure rank features are positive for Elasticsearch
        self.num_episodes = max(1, self.num_episodes)
        self.score_count = max(1, self.score_count)
        self.completed_count = max(1, self.completed_count)
        self.dropped_count = max(1, self.dropped_count)
        self.score = max(0.1, self.score)

    def to_elasticsearch_doc(self) -> dict:
        """Convert the anime entity to an Elasticsearch document."""
        doc = {
            "anime_id": self.anime_id,
            "anime_url": self.anime_url,
            "title": self.title,
            "synopsis": self.synopsis,
            "main_pic": self.main_pic,
            "type": self.type,
            "source_type": self.source_type,
            "num_episodes": self.num_episodes,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "season": self.season,
            "studios": self.studios,
            "genres": self.genres,
            "score": self.score,
            "score_count": self.score_count,
            "score_rank": self.score_rank,
            "popularity_rank": self.popularity_rank,
            "members_count": self.members_count,
            "favorites_count": self.favorites_count,
            "watching_count": self.watching_count,
            "completed_count": self.completed_count,
            "on_hold_count": self.on_hold_count,
            "dropped_count": self.dropped_count,
            "plan_to_watch_count": self.plan_to_watch_count,
            "total_count": self.total_count,
            "score_10_count": self.score_10_count,
            "score_09_count": self.score_09_count,
            "score_08_count": self.score_08_count,
            "score_07_count": self.score_07_count,
            "score_06_count": self.score_06_count,
            "score_05_count": self.score_05_count,
            "score_04_count": self.score_04_count,
            "score_03_count": self.score_03_count,
            "score_02_count": self.score_02_count,
            "score_01_count": self.score_01_count,
            "clubs": self.clubs,
            "pics": self.pics
        }
        
        # Remove None values for cleaner documents
        return {k: v for k, v in doc.items() if v is not None}
