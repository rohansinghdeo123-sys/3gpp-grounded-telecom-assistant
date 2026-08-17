import os
import re

from groq import Groq

from src.config import (
    GROQ_MODEL
)

from src.generator import (
    build_context
)


def citations_are_valid(
    answer,
    evidence_count
):

    matches = re.findall(
        r"\[S(\d+)\]",
        answer
    )


    if not matches:
        return False


    for match in matches:

        number = int(
            match
        )

        if not (
            1
            <= number
            <= evidence_count
        ):

            return False


    return True


def verify_answer(
    question,
    answer,
    evidence
):

    if not citations_are_valid(
        answer,
        len(evidence)
    ):

        return (
            False,
            "Missing or invalid citations."
        )


    api_key = os.getenv(
        "GROQ_API_KEY"
    )


    if not api_key:

        return (
            False,
            "API key unavailable."
        )


    client = Groq(
        api_key=api_key
    )


    context = build_context(
        evidence
    )


    prompt = f"""
You are a strict factual verifier.

Evaluate whether the proposed answer is fully supported by the supplied 3GPP evidence.

Do NOT use outside knowledge.

QUESTION:
{question}

EVIDENCE:
{context}

PROPOSED ANSWER:
{answer}

Return exactly two lines:

VERDICT: PASS

or

VERDICT: FAIL

Then:

REASON: one short reason.

PASS only if the factual claims in the answer are supported by the evidence.
""".strip()


    response = (
        client
        .chat
        .completions
        .create(
            model=GROQ_MODEL,
            temperature=0.0,
            messages=[
                {
                    "role":
                        "user",
                    "content":
                        prompt
                }
            ]
        )
    )


    result = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


    passed = (
        result
        .upper()
        .startswith(
            "VERDICT: PASS"
        )
    )


    return (
        passed,
        result
    )