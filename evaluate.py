from src.pipeline import (
    retrieve_evidence
)


SUPPORTED = [

    "What is the role of the "
    "Access and Mobility "
    "Management Function?",

    "What does the Session "
    "Management Function do?",

    "What is the purpose of "
    "the User Plane Function?",

    "What is UDM?",

    "What is the role of PCF?"
]


UNSUPPORTED = [

    "Who won the FIFA World "
    "Cup in 2022?",

    "What is the capital "
    "of France?",

    "How do I cook pasta?",

    "Explain Python lists.",

    "What is today's weather?"
]


def test_group(
    name,
    questions,
    expected
):

    correct = 0

    print(
        "\n",
        "=" * 70
    )

    print(name)


    for question in questions:

        result = (
            retrieve_evidence(
                question
            )
        )


        evidence = (
            result["evidence"]
        )


        if evidence:

            top = evidence[0]

            semantic = (
                top[
                    "semantic_score"
                ]
            )

            rerank_score = (
                top[
                    "rerank_score"
                ]
            )

        else:

            semantic = 0
            rerank_score = 0


        predicted = (
            result["accepted"]
        )


        if predicted == expected:
            correct += 1


        print(
            "\nQuestion:",
            question
        )

        print(
            "Semantic:",
            round(
                semantic,
                4
            )
        )

        print(
            "Reranker:",
            round(
                rerank_score,
                4
            )
        )

        print(
            "Accepted:",
            predicted
        )


    print(
        "\nCorrect:",
        correct,
        "/",
        len(questions)
    )


    return correct


supported_correct = (
    test_group(
        "SUPPORTED QUESTIONS",
        SUPPORTED,
        True
    )
)


unsupported_correct = (
    test_group(
        "UNSUPPORTED QUESTIONS",
        UNSUPPORTED,
        False
    )
)


total = (
    len(SUPPORTED)
    +
    len(UNSUPPORTED)
)


correct = (
    supported_correct
    +
    unsupported_correct
)


print(
    "\n",
    "=" * 70
)

print(
    "GATE ACCURACY:",
    f"{correct}/{total}"
)