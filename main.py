#  Copyright (c) 2025 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

import os
import time

import torch
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, conlist
from transformers import AutoModelForSequenceClassification

##
# Load the config
##
MODEL_NAME = 'jinaai/jina-reranker-v2-base-multilingual'
VERSION = os.getenv("VERSION") or "unknown"
BUILD_ID = os.getenv("BUILD_ID") or "unknown"
COMMIT_SHA = os.getenv("COMMIT_SHA") or "unknown"
PORT = int(os.getenv("PORT", "8000"))


##
# Models
##
class Document(BaseModel):
    text: str = Field(..., description="The text of the document")
    metadata: dict[str, int | float | str | None] = Field(default_factory=dict, description="Metadata of the document")


class ScoredDocument(Document):
    score: float
    rank: int


class RerankRequest(BaseModel):
    query: str = Field(..., description="The search query")
    documents: conlist(Document, min_length=2) = Field(..., description="List of documents to rerank")
    max_length: int = Field(1024, description="Maximum sequence length for the model")


class RerankResponse(BaseModel):
    ranked_documents: list[ScoredDocument]
    query: str
    computation_time: float = Field(..., description="Time taken to compute the reranking in seconds")


class InfoResponse(BaseModel):
    model_name: str = MODEL_NAME
    device: str
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
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        trust_remote_code=True,
    )
    device = (
        torch.device("cuda") if torch.cuda.is_available()
        else torch.device("mps") if torch.mps.is_available()
        else torch.device("cpu")
    )
    model.eval()
    model.to(device)
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
    return InfoResponse(device=str(device))


@app.post("/rerank", response_model=RerankResponse)
async def rerank(request: RerankRequest = Body(...)):
    start_time = time.time()

    try:
        sentence_pairs = [[request.query, doc.text] for doc in request.documents]

        with torch.no_grad():
            scores = model.compute_score(sentence_pairs, max_length=request.max_length)

        doc_scores = list(zip(request.documents, scores))
        ranked_docs = sorted(doc_scores, key=lambda x: x[1], reverse=True)
        scored_documents = [
            ScoredDocument(
                rank=i + 1,
                score=float(score),
                **doc.model_dump(),
            )
            for i, (doc, score) in enumerate(ranked_docs)
        ]

        return RerankResponse(
            ranked_documents=scored_documents,
            query=request.query,
            computation_time=time.time() - start_time,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during reranking: {str(e)}") from e


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
