import json
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from src.config import (
    CHUNKS_FILE,
    EMBEDDINGS_FILE,
    EMBEDDING_MODEL
)


def load_chunks():

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


chunks = load_chunks()


texts = []

for chunk in chunks:

    texts.append(
        chunk.get(
            "embedding_text",
            chunk["text"]
        )
    )


print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    EMBEDDING_MODEL
)


print(
    "Creating embeddings..."
)


embeddings = (
    model.encode_document(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )
)


embeddings = np.asarray(
    embeddings,
    dtype=np.float32
)


np.save(
    EMBEDDINGS_FILE,
    embeddings
)


print(
    "Number of chunks:",
    len(chunks)
)

print(
    "Embedding shape:",
    embeddings.shape
)

print(
    "Saved embeddings:",
    EMBEDDINGS_FILE
)