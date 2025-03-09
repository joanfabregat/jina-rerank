#  Copyright (c) 2025 Joan Fabrégat <j@fabreg.at>
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, subject to the conditions in the full MIT License.
#  The Software is provided "as is", without warranty of any kind.

import torch
from transformers import AutoModelForSequenceClassification
from .logging import logger

MODEL_NAME = 'jinaai/jina-reranker-v2-base-multilingual'

logger.info(f"Loading model {MODEL_NAME}...")
device = (
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.mps.is_available()
    else "cpu"
)
logger.info(f"Using device: {device}")
try:
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        torch_dtype="auto",
        trust_remote_code=True,
    )
    model.to(device)
    model.eval()
    logger.info(f"Model {MODEL_NAME} loaded successfully")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")
