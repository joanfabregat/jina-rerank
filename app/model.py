#  Copyright (c) 2025 Code Inc. - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Visit <https://www.codeinc.co> for more information

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
