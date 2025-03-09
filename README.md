# Multilingual Reranker API

[![Build and Push to GHCR](https://github.com/joanfabregat/reranker/actions/workflows/build-ghcr.yaml/badge.svg)](https://github.com/joanfabregat/reranker/actions/workflows/build-ghcr.yaml)

A FastAPI service that reranks documents based on query relevance using Jina's multilingual reranker model [`jinaai/jina-reranker-v2-base-multilingual`](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual).

## Overview

This API provides an endpoint for reranking a list of documents based on their relevance to a query. It uses a pre-trained multilingual model to compute similarity scores between the query and each document, then returns the documents sorted by relevance.

## Features

- Rerank documents based on semantic similarity to a query
- Multilingual support through Jina's reranker model
- FastAPI interface with automatic OpenAPI documentation
- Robust error handling and input validation
- Optimized for performance with PyTorch

## Requirements

- Python 3.8+
- PyTorch
- FastAPI
- Uvicorn
- Jina reranker model dependencies

## Installation

```bash
# Clone the repository
git clone https://github.com/codeinc/multilingual-reranker.git
cd multilingual-reranker

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Starting the server

```bash
python -m app
```

The API will be available at `http://localhost:{PORT}` where `PORT` is defined in your config.

### API Endpoints

#### GET /

Returns basic information about the API:

```json
{
  "model_name": "jina-multilingual-reranker",
  "device": "cuda:0",
  "version": "1.0.0",
  "build_id": "abc123",
  "commit_sha": "def456"
}
```

#### POST /rerank

Reranks documents based on query relevance.

Request body:

```json
{
  "query": "What is machine learning?",
  "documents": [
    "Machine learning is a branch of artificial intelligence.",
    "Data science involves extracting knowledge from data.",
    "Natural language processing deals with interactions between computers and human language."
  ]
}
```

Response:

```json
{
  "query": "What is machine learning?",
  "ranked_documents": [
    {
      "document": "Machine learning is a branch of artificial intelligence.",
      "score": 0.95,
      "rank": 1
    },
    {
      "document": "Data science involves extracting knowledge from data.",
      "score": 0.72,
      "rank": 2
    },
    {
      "document": "Natural language processing deals with interactions between computers and human language.",
      "score": 0.64,
      "rank": 3
    }
  ]
}
```

## Configuration

The service can be configured via the following parameters in the `config.py` file:

- `VERSION`: API version string
- `PORT`: Port number for the server
- `BUILD_ID`: Build identifier
- `COMMIT_SHA`: Git commit hash
- Other model-specific configuration

## Error Handling

The API responds with appropriate HTTP status codes:

- `400 Bad Request`: Invalid input (e.g., fewer than 2 documents)
- `500 Internal Server Error`: Issues during reranking process

## Deployment

### Docker

```bash
# Build Docker image
docker build -t jina-reranker .

# Run container
docker run -p 8000:8000 jina-reranker
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```