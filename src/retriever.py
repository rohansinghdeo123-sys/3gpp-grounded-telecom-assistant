import json
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from src.config import (
    CHUNKS_FILE,
    EMBEDDINGS_FILE,
    EMBEDDING_MODEL,
    SEMANTIC_TOP_K
)


_chunks = None
_embeddings = None
_model = None


def get_resources():

    global _chunks
    global _embeddings
    global _model

    if _chunks is None:

        with open(
            CHUNKS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            _chunks = json.load(
                file
            )


    if _embeddings is None:

        _embeddings = np.load(
            EMBEDDINGS_FILE
        )


    if _model is None:

        _model = (
            SentenceTransformer(
                EMBEDDING_MODEL
            )
        )


    return (
        _chunks,
        _embeddings,
        _model
    )


def semantic_search(
    question,
    k=SEMANTIC_TOP_K
):

    chunks, embeddings, model = (
        get_resources()
    )


    query_embedding = (
        model.encode_query(
            question,
            normalize_embeddings=True
        )
    )


    scores = (
        embeddings
        @
        query_embedding
    )


    top_indices = (
        np.argsort(scores)
        [::-1][:k]
    )


    results = []


    for index in top_indices:

        chunk = chunks[
            int(index)
        ]

        results.append({

            **chunk,

            "semantic_score":
                float(
                    scores[index]
                )
        })


    return results


if __name__ == "__main__":

    question = input(
        "Ask a 3GPP question: "
    )

    results = semantic_search(
        question
    )

    for item in results:

        print(
            "\n",
            "=" * 70
        )

        print(
            "Semantic:",
            round(
                item[
                    "semantic_score"
                ],
                4
            )
        )

        print(
            "Section:",
            item["section"]
        )

        print(
            "Title:",
            item[
                "section_title"
            ]
        )

        print(
            item["text"][:600]
        )