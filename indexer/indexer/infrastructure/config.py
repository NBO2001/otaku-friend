import argparse
import os


def parse_args():
    """Parse command line arguments for Elasticsearch configuration."""
    parser = argparse.ArgumentParser(description="Configuration for Elasticsearch connection.")
    
    parser.add_argument(
        "--elasticsearch-host",
        type=str,
        default=os.getenv("ELASTICSEARCH_HOST", "localhost"),
        help="Elasticsearch host address."
    )
    
    parser.add_argument(
        "--elasticsearch-port",
        type=int,
        default=int(os.getenv("ELASTICSEARCH_PORT", 9200)),
        help="Elasticsearch port number."
    )
    
    parser.add_argument(
        "--elasticsearch-username",
        type=str,
        default=os.getenv("ELASTICSEARCH_USERNAME", ""),
        help="Username for Elasticsearch authentication."
    )
    
    parser.add_argument(
        "--elasticsearch-password",
        type=str,
        default=os.getenv("ELASTICSEARCH_PASSWORD", ""),
        help="Password for Elasticsearch authentication."
    )
    
    # Parse only known args to avoid conflicts with main.py args
    args, _ = parser.parse_known_args()
    return args