# Multilingual Reranker API

[![Build and Push to GHCR and Docker Hub](https://github.com/joanfabregat/jina-rerank/actions/workflows/build.yaml/badge.svg)](https://github.com/joanfabregat/jina-rerank/actions/workflows/build.yaml)

A FastAPI service that provides document reranking capabilities based on query relevance using the [`jinaai/jina-reranker-v2-base-multilingual`](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) model.

## Overview

This API allows you to rerank a list of documents based on their relevance to a given query. It utilizes a cross-encoder reranking model from Jina AI that supports multiple languages.

## Features

- Multilingual support for document reranking
- REST API with FastAPI
- Automatic API documentation
- Docker support

## Requirements

- Python 3.8+
- FastAPI
- Pydantic
- fastembed
- uvicorn (for serving)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/codeinc/multilingual-reranker.git
   cd multilingual-reranker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the model:
   ```bash
   python main.py download
   ```

## Usage

### Starting the Server

```bash
python main.py serve
```

Or with custom port:
```bash
PORT=8080 python main.py serve
```

### Docker

```bash
docker build -t multilingual-reranker .
docker run -p 8000:8000 multilingual-reranker
```

## API Endpoints

### GET /

Redirects to the API documentation.

### GET /info

Returns information about the service, including:
- Model name
- Version
- Build ID
- Commit SHA

### POST /rerank

Reranks documents based on their relevance to a query.

#### Request Body

```json
{
  "query": "Your search query",
  "documents": [
    {
      "text": "Document content 1",
      "metadata": {"source": "wiki", "id": "12345"}
    },
    {
      "text": "Document content 2",
      "metadata": {"source": "web", "id": "67890"}
    }
  ],
  "max_length": 1024
}
```

#### Response

```json
[
  {
    "text": "Document content 2",
    "metadata": {"source": "web", "id": "67890"},
    "score": 0.92,
    "rank": 1
  },
  {
    "text": "Document content 1",
    "metadata": {"source": "wiki", "id": "12345"},
    "score": 0.75,
    "rank": 2
  }
]
```

## Environment Variables

- `VERSION`: Service version
- `BUILD_ID`: Build identifier
- `COMMIT_SHA`: Commit identifier
- `PORT`: Server port (default: 8000)

## License

Copyright (c) 2025 Code Inc. - All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.

Visit [Code Inc](https://www.codeinc.co) for more information.