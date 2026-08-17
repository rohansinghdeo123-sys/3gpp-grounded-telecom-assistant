from pathlib import Path
import os

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")


CHUNKS_FILE = ROOT_DIR / "data" / "processed" / "chunks.json"

EMBEDDINGS_FILE = (
    ROOT_DIR
    / "indexes"
    / "chunk_embeddings.npy"
)


EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


SEMANTIC_TOP_K = int(
    os.getenv(
        "SEMANTIC_TOP_K",
        "12"
    )
)


FINAL_TOP_K = int(
    os.getenv(
        "FINAL_TOP_K",
        "4"
    )
)


MIN_SEMANTIC_SCORE = float(
    os.getenv(
        "MIN_SEMANTIC_SCORE",
        "0.25"
    )
)


MIN_RERANK_SCORE = float(
    os.getenv(
        "MIN_RERANK_SCORE",
        "0.60"
    )
)