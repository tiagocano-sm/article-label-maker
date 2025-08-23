# Article Classification API

A FastAPI-based service for classifying articles based on their title and abstract using machine learning techniques.

## Features

- **Single Article Classification**: Classify individual articles with title and abstract
- **Batch CSV Processing**: Process multiple articles from CSV files
- **RESTful API**: Clean, documented API endpoints
- **File Upload/Download**: Handle CSV file processing with automatic downloads

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn main:app --reload
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### POST /classify_article

Classify a single article based on title and abstract.

**Request Body:**
```json
{
  "title": "Deep Learning for Computer Vision",
  "abstract": "This paper presents a novel approach to computer vision using deep learning techniques..."
}
```

**Response:**
```json
{
  "title": "Deep Learning for Computer Vision",
  "labels": {
    "deep_learning": 0.892,
    "computer_vision": 0.756,
    "machine_learning": 0.634
  }
}
```

### POST /classify_articles_in_csv

Upload a CSV file with articles and get back a processed version with labels.

**Request:** Multipart form with CSV file containing `title` and `abstract` columns.

**Response:**
```json
{
  "message": "CSV processed successfully",
  "processed_rows": 150,
  "output_filename": "articles_classified.csv"
}
```

### GET /download/{filename}

Download a processed CSV file.

## CSV Format

Your CSV file should have the following columns:

```csv
title,abstract
"Article Title 1","Article abstract text..."
"Article Title 2","Article abstract text..."
```

The processed CSV will include an additional `labels` column:

```csv
title,abstract,labels
"Article Title 1","Article abstract text...","deep_learning:0.892;computer_vision:0.756"
"Article Title 2","Article abstract text...","machine_learning:0.734;statistics:0.623"
```

## Project Structure

```
api/
├── main.py              # FastAPI application
├── schemas.py           # Pydantic models
├── services.py          # Classification service
├── csv_processor.py     # CSV processing logic
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Development

### Running Tests

```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

```bash
# Install linting tools
uv add --dev black isort flake8

# Format code
black .
isort .

# Lint code
flake8 .
```

## Configuration

The API can be configured through environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: False)

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Production Server

```bash
# Install production dependencies
uv add gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## License

MIT License
