import torch

from sentence_transformers import (
    CrossEncoder
)

from src.config import (
    RERANKER_MODEL,
    FINAL_TOP_K,
    MIN_SEMANTIC_SCORE,
    MIN_RERANK_SCORE
)


_reranker = None


def get_reranker():

    global _reranker

    if _reranker is None:

        _reranker = CrossEncoder(
            RERANKER_MODEL,
            activation_fn=(
                torch.nn.Sigmoid()
            )
        )

    return _reranker


def rerank(
    question,
    candidates,
    k=FINAL_TOP_K
):

    if not candidates:
        return []


    model = get_reranker()


    pairs = []

    for item in candidates:

        text = item.get(
            "embedding_text",
            item["text"]
        )

        pairs.append(
            (
                question,
                text
            )
        )


    scores = model.predict(
        pairs,
        show_progress_bar=False
    )


    results = []


    for candidate, score in zip(
        candidates,
        scores
    ):

        item = dict(
            candidate
        )

        item[
            "rerank_score"
        ] = float(score)

        results.append(
            item
        )


    results.sort(
        key=lambda item:
            item["rerank_score"],
        reverse=True
    )


    return results[:k]


def has_sufficient_evidence(
    results
):

    if not results:
        return False


    top = results[0]


    semantic_ok = (
        top["semantic_score"]
        >=
        MIN_SEMANTIC_SCORE
    )


    rerank_ok = (
        top["rerank_score"]
        >=
        MIN_RERANK_SCORE
    )


    return (
        semantic_ok
        and
        rerank_ok
    )