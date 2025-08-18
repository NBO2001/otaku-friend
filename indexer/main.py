#!/usr/bin/env python3
"""
Anime Indexer Application

A Domain-Driven Design (DDD) application for indexing anime data into Elasticsearch.
This application reads anime data from CSV files and indexes it into Elasticsearch
with proper logging and error handling.

Architecture:
- Domain Layer: Contains business entities, repositories interfaces, and domain services
- Application Layer: Contains use cases that orchestrate domain objects
- Infrastructure Layer: Contains concrete implementations of repositories and external services

Usage:
    python main.py [--log-level DEBUG] [--log-file anime_indexer.log]
"""

import argparse
import sys
from pathlib import Path

from indexer.infrastructure.container import Container


def setup_cli_args():
    """Set up command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Anime Indexer - Index anime data into Elasticsearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--csv-file",
        type=str,
        default="./downloads/anime.csv",
        help="Path to the CSV file containing anime data (default: ./downloads/anime.csv)"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to log file (optional, logs to console by default)"
    )
    
    return parser.parse_args()


def main():
    """Main application entry point."""
    
    # Parse command line arguments
    cli_args = setup_cli_args()
    
    # Initialize dependency injection container with logging configuration
    container = Container(
        log_level=cli_args.log_level,
        log_file=cli_args.log_file
    )
    
    logger = container.logger
    
    try:
        logger.info("=" * 60)
        logger.info("Anime Indexer Application Starting")
        logger.info("=" * 60)
        
        # Validate CSV file path
        csv_file_path = Path(cli_args.csv_file)
        if not csv_file_path.exists():
            logger.error(f"CSV file not found: {csv_file_path}")
            logger.error("Please ensure the CSV file exists or specify a different path with --csv-file")
            sys.exit(1)
        
        logger.info(f"CSV file: {csv_file_path}")
        logger.info(f"Log level: {cli_args.log_level}")
        if cli_args.log_file:
            logger.info(f"Log file: {cli_args.log_file}")
        
        # Execute the use case
        use_case = container.index_anime_data_use_case
        success = use_case.execute(str(csv_file_path))
        
        if success:
            logger.info("=" * 60)
            logger.info("Anime indexing completed successfully!")
            logger.info("=" * 60)
            sys.exit(0)
        else:
            logger.error("=" * 60)
            logger.error("Anime indexing failed!")
            logger.error("=" * 60)
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(130)
        
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
