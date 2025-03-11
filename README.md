# Multilingual Reranker API

[![Build and Push to GHCR and Docker Hub](https://github.com/joanfabregat/jina-rerank/actions/workflows/build.yaml/badge.svg)](https://github.com/joanfabregat/jina-rerank/actions/workflows/build.yaml)

A FastAPI-based service that provides document reranking capabilities based on query relevance using the
[`jinaai/jina-reranker-v2-base-multilingual`](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) model.

## Overview

This API enables users to rerank a collection of documents based on their relevance to a specific query. It leverages a
multilingual reranker model that can handle content in multiple languages.

## Features

- **Document Reranking**: Rerank documents based on their relevance to a search query
- **Multilingual Support**: Works with content in multiple languages
- **Metadata Preservation**: Maintains document metadata throughout the reranking process
- **Performance Metrics**: Includes computation time in responses

## Usage

### Starting the Server

The recommended way to run this service is using Docker.

```shell
docker run -p 8000:8000 joanfabregat/jina-rerank:latest
```

Documentation for the API can be found at `/docs` or `/redoc` when running the server.

### API Endpoints

#### GET `/info`

Returns information about the API, including model name, version, build ID, and commit SHA.

**Response:**

```json
{
  "model_name": "jinaai/jina-reranker-v2-base-multilingual",
  "version": "your-version",
  "build_id": "your-build-id",
  "commit_sha": "your-commit-sha"
}
```

#### POST `/rerank`

Reranks a list of documents based on their relevance to a query.

**Request Body:**

```json
{
  "query": "your search query",
  "documents": [
    {
      "text": "document content 1",
      "metadata": {
        "source": "web",
        "id": 123
      }
    },
    {
      "text": "document content 2",
      "metadata": {
        "source": "database",
        "id": 456
      }
    }
  ],
  "max_length": 1024
}
```

**Response:**

```json
[
  {
    "text": "document content 2",
    "metadata": {
      "source": "database",
      "id": 456
    },
    "score": 0.95,
    "rank": 1
  },
  {
    "text": "document content 1",
    "metadata": {
      "source": "web",
      "id": 123
    },
    "score": 0.82,
    "rank": 2
  }
]
```

## Environment Variables

- `PORT`: Port to run the server on (default: 8000)

## License

This project is licensed under the MIT License - see the license notice in the code for details.

## Author

Developed by Joan Fabrégat, j@fabreg.at