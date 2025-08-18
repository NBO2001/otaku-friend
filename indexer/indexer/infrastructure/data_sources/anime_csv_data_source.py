import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from indexer.domain.entities.anime import Anime
from indexer.domain.repositories.csv_data_source import CsvDataSource


class AnimeCsvDataSource(CsvDataSource):
    """CSV data source implementation for reading anime data."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def read_anime_data(self, file_path: str) -> List[Anime]:
        """Read anime data from CSV file and return list of Anime entities."""
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        self.logger.info(f"Reading anime data from: {file_path}")
        
        animes = []
        failed_count = 0
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter='\t')
                
                for row_num, row in enumerate(csv_reader, start=1):
                    try:
                        anime = self._row_to_anime(row)
                        animes.append(anime)
                        
                        if row_num % 1000 == 0:
                            self.logger.info(f"Processed {row_num} rows...")
                            
                    except Exception as e:
                        failed_count += 1
                        self.logger.warning(f"Failed to process row {row_num}: {e}")
                        
                        # Log the problematic row for debugging
                        if failed_count <= 5:  # Only log first 5 failures
                            self.logger.debug(f"Problematic row data: {row}")
                        
                        continue
            
            self.logger.info(f"Successfully read {len(animes)} anime records, {failed_count} failed")
            return animes
            
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {e}")
            raise
    
    def _row_to_anime(self, row: dict) -> Anime:
        """Convert a CSV row to an Anime entity."""
        
        # Process integer fields
        integer_fields = [
            'anime_id', 'num_episodes', 'popularity_rank', 'members_count',
            'favorites_count', 'watching_count', 'completed_count', 'on_hold_count',
            'dropped_count', 'plan_to_watch_count', 'total_count',
            'score_10_count', 'score_09_count', 'score_08_count', 'score_07_count',
            'score_06_count', 'score_05_count', 'score_04_count', 'score_03_count',
            'score_02_count', 'score_01_count', 'score_count', 'score_rank'
        ]
        
        for field in integer_fields:
            if row.get(field):
                try:
                    row[field] = int(row[field])
                except (ValueError, TypeError):
                    row[field] = 0
            else:
                row[field] = 0
        
        # Process rank feature fields (must be positive)
        rank_fields = ['dropped_count', 'score_count', 'completed_count', 'num_episodes']
        for field in rank_fields:
            if row.get(field):
                value = int(row[field]) if row[field] else 1
                row[field] = max(1, value)
            else:
                row[field] = 1
        
        # Process score field
        if row.get('score'):
            try:
                score = float(row['score'])
                row['score'] = max(0.1, score)
            except (ValueError, TypeError):
                row['score'] = 0.1
        else:
            row['score'] = 0.1
        
        # Process date fields
        start_date = self._parse_date(row.get('start_date'))
        end_date = self._parse_date(row.get('end_date'))
        
        # Create Anime entity
        return Anime(
            anime_id=row['anime_id'],
            anime_url=row.get('anime_url') or None,
            title=row.get('title', '').strip(),
            synopsis=row.get('synopsis', '').strip(),
            main_pic=row.get('main_pic') or None,
            type=row.get('type') or None,
            source_type=row.get('source_type') or None,
            num_episodes=row['num_episodes'],
            status=row.get('status') or None,
            start_date=start_date,
            end_date=end_date,
            season=row.get('season') or None,
            studios=row.get('studios') or None,
            genres=row.get('genres') or None,
            score=row['score'],
            score_count=row['score_count'],
            score_rank=row['score_rank'],
            popularity_rank=row['popularity_rank'],
            members_count=row['members_count'],
            favorites_count=row['favorites_count'],
            watching_count=row['watching_count'],
            completed_count=row['completed_count'],
            on_hold_count=row['on_hold_count'],
            dropped_count=row['dropped_count'],
            plan_to_watch_count=row['plan_to_watch_count'],
            total_count=row['total_count'],
            score_10_count=row['score_10_count'],
            score_09_count=row['score_09_count'],
            score_08_count=row['score_08_count'],
            score_07_count=row['score_07_count'],
            score_06_count=row['score_06_count'],
            score_05_count=row['score_05_count'],
            score_04_count=row['score_04_count'],
            score_03_count=row['score_03_count'],
            score_02_count=row['score_02_count'],
            score_01_count=row['score_01_count'],
            clubs=row.get('clubs') or None,
            pics=row.get('pics') or None
        )
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime object."""
        if not date_str or not date_str.strip():
            return None
        
        try:
            # Handle the format from CSV: "YYYY-MM-DD HH:MM:SS"
            if ' ' in date_str:
                # Replace space with 'T' for ISO format
                date_str = date_str.replace(' ', 'T')
            
            return datetime.fromisoformat(date_str)
            
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Could not parse date '{date_str}': {e}")
            return None
