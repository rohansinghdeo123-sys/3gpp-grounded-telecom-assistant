import streamlit as st

from src.pipeline import (
    answer_question
)


st.set_page_config(
    page_title=(
        "3GPP Grounded "
        "Telecom Assistant"
    ),
    page_icon="📡",
    layout="wide"
)


st.title(
    "📡 3GPP Grounded "
    "Telecom Assistant"
)


st.caption(
    "Answers are grounded in "
    "indexed 3GPP standards. "
    "Unsupported questions are "
    "rejected."
)


if "messages" not in (
    st.session_state
):

    st.session_state.messages = []


for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


        result = message.get(
            "result"
        )


        if (
            result
            and
            result.get(
                "evidence"
            )
        ):

            with st.expander(
                "View retrieved "
                "3GPP evidence"
            ):

                for i, item in (
                    enumerate(
                        result[
                            "evidence"
                        ],
                        start=1
                    )
                ):

                    st.markdown(
                        f"### S{i}"
                    )

                    st.write(
                        "Source:",
                        item[
                            "source"
                        ]
                    )

                    st.write(
                        "Section:",
                        item[
                            "section"
                        ]
                    )

                    st.write(
                        "Title:",
                        item[
                            "section_title"
                        ]
                    )

                    st.write(
                        "Semantic score:",
                        round(
                            item[
                                "semantic_score"
                            ],
                            4
                        )
                    )

                    st.write(
                        "Reranker score:",
                        round(
                            item[
                                "rerank_score"
                            ],
                            4
                        )
                    )

                    st.write(
                        item["text"]
                    )

                    st.divider()


question = st.chat_input(
    "Ask a question about "
    "3GPP / 5G standards..."
)


if question:

    user_message = {
        "role": "user",
        "content": question
    }


    st.session_state.messages.append(
        user_message
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Retrieving and "
            "verifying 3GPP "
            "evidence..."
        ):

            result = (
                answer_question(
                    question
                )
            )


        st.markdown(
            result["answer"]
        )


        if result[
            "accepted"
        ]:

            st.success(
                "Grounded answer "
                "verified."
            )

        else:

            st.warning(
                "Insufficient "
                "verified 3GPP "
                "evidence."
            )


        if result[
            "evidence"
        ]:

            with st.expander(
                "View retrieved "
                "3GPP evidence"
            ):

                for i, item in (
                    enumerate(
                        result[
                            "evidence"
                        ],
                        start=1
                    )
                ):

                    st.markdown(
                        f"### S{i}"
                    )

                    st.write(
                        f"**Source:** "
                        f"{item['source']}"
                    )

                    st.write(
                        f"**Section:** "
                        f"{item['section']}"
                    )

                    st.write(
                        f"**Title:** "
                        f"{item['section_title']}"
                    )

                    st.write(
                        "**Semantic "
                        "score:**",
                        round(
                            item[
                                "semantic_score"
                            ],
                            4
                        )
                    )

                    st.write(
                        "**Reranker "
                        "score:**",
                        round(
                            item[
                                "rerank_score"
                            ],
                            4
                        )
                    )

                    st.write(
                        item["text"]
                    )

                    st.divider()


    assistant_message = {
        "role":
            "assistant",

        "content":
            result["answer"],

        "result":
            result
    }


    st.session_state.messages.append(
        assistant_message
    )