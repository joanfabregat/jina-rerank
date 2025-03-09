#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

from pydantic import BaseModel, Field


class Document(BaseModel):
    text: str = Field(..., description="The text of the document")
    metadata: dict[str, str] = Field({}, description="Metadata of the document")


class RerankRequest(BaseModel):
    query: str = Field(..., description="The search query")
    documents: list[Document] = Field(..., description="List of documents to rerank", min_items=1)
    max_length: int = Field(1024, description="Maximum sequence length for the model")


class ScoredDocument(BaseModel):
    document: Document
    score: float
    rank: int


class RerankResponse(BaseModel):
    ranked_documents: list[ScoredDocument]
    query: str
    computation_time: float = Field(..., description="Time taken to compute the reranking in seconds")
