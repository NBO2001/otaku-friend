# Anime Indexer

A Domain-Driven Design (DDD) application for indexing anime data into Elasticsearch with comprehensive logging and error handling.

## 🏗️ Architecture

This application follows Domain-Driven Design principles with a clean separation of concerns:

```
indexer/
├── indexer/
│   ├── domain/                    # Domain Layer - Business Logic
│   │   ├── entities/
│   │   │   └── anime.py          # Anime domain entity with validation
│   │   ├── repositories/
│   │   │   ├── anime_repository.py      # Abstract repository interface
│   │   │   └── csv_data_source.py       # Abstract CSV data source interface
│   │   └── services/
│   │       └── anime_indexing_service.py # Domain service for business logic
│   ├── application/               # Application Layer - Use Cases
│   │   └── use_cases/
│   │       └── index_anime_data_use_case.py # Application orchestration
│   └── infrastructure/           # Infrastructure Layer - External Concerns
│       ├── logging/
│       │   └── logger_config.py         # Logging configuration
│       ├── repositories/
│       │   └── elasticsearch_anime_repository.py # Elasticsearch implementation
│       ├── data_sources/
│       │   └── anime_csv_data_source.py # CSV data source implementation
│       ├── config.py                    # Configuration management
│       └── container.py                 # Dependency injection container
└── main.py                       # Application entry point
```

### 🎯 Design Principles

- **Domain Layer**: Contains business entities, repository interfaces, and domain services
- **Application Layer**: Contains use cases that orchestrate domain objects
- **Infrastructure Layer**: Contains concrete implementations and external service integrations
- **Dependency Injection**: Clean dependency management through the Container pattern
- **Interface Segregation**: Abstract interfaces for repositories and data sources

## 🚀 Features

- ✅ **Bulk Indexing**: Efficient batch processing for optimal performance
- ✅ **Domain Validation**: Business rules enforced at the entity level
- ✅ **Comprehensive Logging**: Structured logging with configurable levels
- ✅ **Error Handling**: Robust error handling with fallback mechanisms
- ✅ **CLI Interface**: Command-line interface with multiple configuration options
- ✅ **Clean Architecture**: Testable and maintainable code structure

## 📋 Prerequisites

- Python 3.12+
- Poetry for dependency management
- Docker and Docker Compose (for Elasticsearch and Kibana)
- CSV file with anime data

## 🛠️ Installation

1. **Clone the repository and navigate to the indexer directory:**
   ```bash
   cd indexer
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Start Elasticsearch and Kibana services:**
   ```bash
   cd .. && docker-compose up -d
   ```

4. **Wait for services to be ready:**
   ```bash
   # Check Elasticsearch health
   curl -s "http://localhost:9200/_cluster/health"
   ```

## 🎮 Usage

### Basic Usage

```bash
# Index anime data with default settings
poetry run python main.py
```

### Advanced Usage

```bash
# With debug logging and log file
poetry run python main.py --log-level DEBUG --log-file anime_indexer.log

# With custom CSV file path
poetry run python main.py --csv-file /path/to/your/anime.csv

# Combination of options
poetry run python main.py --csv-file data/anime.csv --log-level INFO --log-file logs/indexer.log
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--csv-file` | Path to the CSV file containing anime data | `./downloads/anime.csv` |
| `--log-level` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `--log-file` | Path to log file (optional, logs to console by default) | Console only |

### Help

```bash
poetry run python main.py --help
```

## 📊 Expected CSV Format

The application expects a CSV file with anime data containing the following columns:

- `anime_id`: Unique identifier for the anime
- `Name`: Anime title
- `English name`: English title (if available)
- `Other name`: Alternative names
- `Score`: Rating score
- `Genres`: Comma-separated list of genres
- `Synopsis`: Description of the anime
- `Type`: Anime type (TV, Movie, OVA, etc.)
- `Episodes`: Number of episodes
- `Aired`: Air date information
- `Status`: Current status (Finished Airing, Currently Airing, etc.)
- `Source`: Source material (Manga, Light Novel, etc.)
- `Duration`: Episode duration
- `Rating`: Content rating
- `Rank`: Popularity rank
- `Popularity`: Popularity score
- `Favorites`: Number of favorites
- `Scored By`: Number of users who scored
- `Members`: Number of members

## 📁 Services

### Elasticsearch
- **URL**: http://localhost:9200
- **Index**: `anime` (created automatically)
- **Health Check**: `curl http://localhost:9200/_cluster/health`

### Kibana
- **URL**: http://localhost:5601
- **Use for**: Data visualization and exploration

## 📝 Logging

The application provides comprehensive logging with the following features:

### Log Levels
- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for handled exceptions
- **CRITICAL**: Critical errors that may cause application termination

### Log Format
```
2025-08-18 17:16:32,596 - anime_indexer - INFO - main.py:72 - main() - Application Starting
```

Format: `timestamp - logger_name - level - file:line - function() - message`

### Log Outputs
- **Console**: Always enabled with colored output
- **File**: Optional, specified with `--log-file` parameter

## 🏛️ Domain Model

### Anime Entity

The `Anime` entity represents the core business object with the following features:

- **Validation**: Ensures required fields are present and valid
- **Business Rules**: Enforces domain constraints (e.g., positive scores, valid episode counts)
- **Elasticsearch Mapping**: Converts domain objects to Elasticsearch documents

```python
@dataclass
class Anime:
    anime_id: str
    name: str
    english_name: Optional[str] = None
    other_name: Optional[str] = None
    score: Optional[float] = None
    genres: List[str] = field(default_factory=list)
    synopsis: Optional[str] = None
    # ... other fields
```

## 🔧 Configuration

The application uses environment-based configuration with sensible defaults:

- **Elasticsearch Host**: `localhost`
- **Elasticsearch Port**: `9200`
- **Index Name**: `anime`
- **Batch Size**: `1000` (for bulk indexing)
- **Request Timeout**: `60` seconds

## 🧪 Testing

To test the application:

1. **Ensure services are running:**
   ```bash
   docker-compose up -d
   ```

2. **Run with debug logging:**
   ```bash
   poetry run python main.py --log-level DEBUG
   ```

3. **Verify data in Elasticsearch:**
   ```bash
   curl "http://localhost:9200/anime/_count"
   ```

4. **Check Kibana dashboard:**
   ```bash
   open http://localhost:5601
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused Error**
   ```
   Solution: Ensure Elasticsearch is running with `docker-compose up -d`
   ```

2. **CSV File Not Found**
   ```
   Solution: Verify the CSV file path or use --csv-file to specify correct path
   ```

3. **Permission Denied**
   ```
   Solution: Check file permissions for CSV file and log directory
   ```

4. **Version Compatibility**
   ```
   Solution: Ensure Elasticsearch client version matches server version (8.x)
   ```

### Health Checks

```bash
# Check Elasticsearch health
curl "http://localhost:9200/_cluster/health"

# Check if index exists
curl "http://localhost:9200/anime"

# Count indexed documents
curl "http://localhost:9200/anime/_count"
```

## 📈 Performance

- **Bulk Indexing**: Processes data in batches of 1000 documents
- **Memory Efficient**: Streams CSV data to avoid loading entire file in memory
- **Connection Pooling**: Reuses Elasticsearch connections for better performance
- **Error Recovery**: Continues processing even if individual documents fail

## 🤝 Contributing

1. Follow the DDD architecture principles
2. Add appropriate logging for new features
3. Include error handling for external service calls
4. Update tests for new functionality
5. Document any new configuration options

## 📄 License

This project is part of the Otaku Friend application.

---

**Happy Indexing! 🎌✨**