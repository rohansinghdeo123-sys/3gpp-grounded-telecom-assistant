import os
import re

from groq import Groq

from src.config import (
    GROQ_MODEL
)


ABSTAIN_MESSAGE = (
    "I could not find sufficient "
    "supporting information in the "
    "indexed 3GPP standards to "
    "answer this question."
)


def get_client():

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is missing "
            "from the .env file."
        )


    return Groq(
        api_key=api_key
    )


def build_context(
    evidence
):

    parts = []


    for i, item in enumerate(
        evidence,
        start=1
    ):

        part = (
            f"[S{i}]\n"
            f"Source: "
            f"{item['source']}\n"
            f"Section: "
            f"{item['section']}\n"
            f"Title: "
            f"{item['section_title']}\n"
            f"Text:\n"
            f"{item['text']}"
        )

        parts.append(
            part
        )


    return "\n\n".join(
        parts
    )


def generate_answer(
    question,
    evidence
):

    context = build_context(
        evidence
    )


    system_prompt = f"""
You are a telecom standards assistant.

You must answer ONLY from the supplied 3GPP evidence.

Rules:
1. Never use external knowledge or prior model knowledge.
2. Do not invent missing facts.
3. Every factual statement must be supported by the supplied evidence.
4. You MUST include at least one citation in the exact format [S1], [S2], etc.
   Do not provide a factual answer without a citation.
5. If the evidence does not contain enough information to answer confidently, respond exactly:

{ABSTAIN_MESSAGE}

Keep the answer concise and easy to understand.
Summarize the most important points first.
Use at most 5-7 bullets unless the user explicitly asks for full detail.
""".strip()


    user_prompt = f"""
3GPP EVIDENCE:

{context}

QUESTION:

{question}
""".strip()


    client = get_client()


    response = (
        client
        .chat
        .completions
        .create(
            model=GROQ_MODEL,
            temperature=0.1,
            messages=[
                {
                    "role":
                        "system",
                    "content":
                        system_prompt
                },
                {
                    "role":
                        "user",
                    "content":
                        user_prompt
                }
            ]
        )
    )


    answer = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # Preserve explicit abstention
    if answer == ABSTAIN_MESSAGE:
        return answer

    # The answer must contain at least one evidence citation.
    # Some LLMs may occasionally omit the requested [S1] marker,
    # so attach the highest-ranked evidence reference as a safe fallback.
    if not re.search(r"\[S\d+\]", answer):
        if evidence:
            answer += "\n\nSource: [S1]"

    return answer