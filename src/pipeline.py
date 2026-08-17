from src.config import (
    SEMANTIC_TOP_K,
    FINAL_TOP_K
)

from src.retriever import (
    semantic_search
)

from src.reranker import (
    rerank,
    has_sufficient_evidence
)

from src.generator import (
    generate_answer,
    ABSTAIN_MESSAGE
)

from src.verifier import (
    verify_answer
)


def retrieve_evidence(
    question
):

    candidates = (
        semantic_search(
            question,
            k=SEMANTIC_TOP_K
        )
    )


    evidence = rerank(
        question,
        candidates,
        k=FINAL_TOP_K
    )


    accepted = (
        has_sufficient_evidence(
            evidence
        )
    )


    return {
        "accepted":
            accepted,

        "candidates":
            candidates,

        "evidence":
            evidence
    }


def answer_question(
    question
):

    retrieval = (
        retrieve_evidence(
            question
        )
    )


    evidence = (
        retrieval[
            "evidence"
        ]
    )


    if not (
        retrieval[
            "accepted"
        ]
    ):

        return {
            "accepted": False,
            "answer":
                ABSTAIN_MESSAGE,
            "evidence":
                evidence,
            "verification":
                "Rejected by confidence gate."
        }


    answer = generate_answer(
        question,
        evidence
    )


    if (
        answer.strip()
        ==
        ABSTAIN_MESSAGE
    ):

        return {
            "accepted": False,
            "answer":
                ABSTAIN_MESSAGE,
            "evidence":
                evidence,
            "verification":
                "Generator abstained."
        }


    verified, reason = (
        verify_answer(
            question,
            answer,
            evidence
        )
    )


    if not verified:

        return {
            "accepted": False,
            "answer":
                ABSTAIN_MESSAGE,
            "evidence":
                evidence,
            "verification":
                reason
        }


    return {
        "accepted": True,
        "answer":
            answer,
        "evidence":
            evidence,
        "verification":
            reason
    }