#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

import os

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import RedirectResponse
from fastembed.rerank.cross_encoder import TextCrossEncoder
from pydantic import BaseModel, Field, conlist

##
# Load the config
##
MODEL_NAME = 'jinaai/jina-reranker-v2-base-multilingual'
COMPUTE_DEVICE = os.getenv("COMPUTE_DEVICE") or "cpu"
VERSION = os.getenv("VERSION") or "unknown"
BUILD_ID = os.getenv("BUILD_ID") or "unknown"
COMMIT_SHA = os.getenv("COMMIT_SHA") or "unknown"
PORT = int(os.getenv("PORT") or "8000")
PROVIDERS: dict[str, list[str]] = {
    "cpu": ["CPUExecutionProvider"],
    "gpu": ["CUDAExecutionProvider"],
    # https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html
    "coreml": [('CoreMLExecutionProvider', {
        "ModelFormat": "MLProgram",
        "MLComputeUnits": "ALL",
        # "RequireStaticInputShapes": "0", 
        # "EnableOnSubgraphs": "0"
    })]
}


##
# Models
##
class RerankRequest(BaseModel):
    query: str = Field(..., description="The search query")
    documents: conlist(str, min_length=2) = Field(..., description="List of documents to rerank")
    max_length: int = Field(1024, description="Maximum sequence length for the model")


class InfoResponse(BaseModel):
    model_name: str = MODEL_NAME
    compute_device: str = COMPUTE_DEVICE
    version: str = VERSION
    build_id: str = BUILD_ID
    commit_sha: str = COMMIT_SHA


##
# Create the FastAPI app
##
app = FastAPI(
    title="Multilingual Reranker API",
    description=f"API for reranking documents based on query relevance using {MODEL_NAME}",
    version=VERSION,
)

##
# Load the model
##
try:
    print(f"Loading model {MODEL_NAME}...")

    # Select the provider
    provider = PROVIDERS[COMPUTE_DEVICE]
    if not provider:
        raise ValueError(f"Invalid compute device: {COMPUTE_DEVICE}")

    # Load the model
    reranker = TextCrossEncoder(model_name=MODEL_NAME, providers=provider)

    print(f"Model {MODEL_NAME} loaded successfully")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")


##
# Routes
##
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/info", response_model=InfoResponse)
async def info():
    return InfoResponse()


@app.post("/rerank", response_model=list[float])
async def rerank(request: RerankRequest = Body(...)):
    try:
        # Compute the embeddings
        scores = list(
            reranker.rerank(
                request.query,
                documents=request.documents
            )
        )
        return scores

    except Exception as e_:
        raise HTTPException(status_code=500, detail=f"Error during reranking: {str(e_)}") from e_


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "serve"

    # Start the server
    if command == "serve":
        import uvicorn

        uvicorn.run("main:app", host="0.0.0.0", port=PORT)

    # Download the model
    elif command == "download":
        sys.exit(0)
