#  Copyright (c) 2025 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

from pydantic import BaseModel, Field


class RerankRequest(BaseModel):
    query: str = Field(..., description="The search query")
    documents: list[str] = Field(..., description="List of documents to rerank", min_items=1)
    max_length: int = Field(1024, description="Maximum sequence length for the model")


class ScoredDocument(BaseModel):
    document: str
    score: float
    rank: int


class RerankResponse(BaseModel):
    ranked_documents: list[ScoredDocument]
    query: str
