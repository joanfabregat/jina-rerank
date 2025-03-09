#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

import torch
import uvicorn
from fastapi import FastAPI, HTTPException, Body
import time

from .config import VERSION, PORT, BUILD_ID, COMMIT_SHA
from .model import model, MODEL_NAME
from .types import RerankRequest, RerankResponse, ScoredDocument

app = FastAPI(
    title="Multilingual Reranker API",
    description="API for reranking documents based on query relevance using Jina's multilingual reranker",
    version=VERSION,
)


@app.post("/rerank", response_model=RerankResponse)
async def rerank(request: RerankRequest = Body(...)):
    start_time = time.time()

    try:
        # Create sentence pairs for the model
        sentence_pairs = [[request.query, doc.text] for doc in request.documents]

        with torch.no_grad():
            scores = model.compute_score(sentence_pairs, max_length=1024)

        # Create tuples of (document with metadata, score) and sort by score
        doc_scores = list(zip(request.documents, scores))
        ranked_docs = sorted(doc_scores, key=lambda x: x[1], reverse=True)

        # Create the response with ranked documents (preserving metadata)
        scored_documents = [
            ScoredDocument(
                document=doc,
                score=float(score),
                rank=i + 1
            )
            for i, (doc, score) in enumerate(ranked_docs)
        ]

        return RerankResponse(
            ranked_documents=scored_documents,
            query=request.query,
            computation_time=time.time() - start_time,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during reranking: {str(e)}")


@app.get("/")
async def root():
    return {
        "model_name": MODEL_NAME,
        "version": VERSION,
        "build_id": BUILD_ID,
        "commit_sha": COMMIT_SHA,
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(PORT), reload=True)
