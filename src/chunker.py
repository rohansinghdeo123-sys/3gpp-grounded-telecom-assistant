from pathlib import Path
import json


INPUT_FILE = Path(
    "data/processed/documents.json"
)

OUTPUT_FILE = Path(
    "data/processed/chunks.json"
)


CHUNK_SIZE = 1200
OVERLAP = 200


def load_documents():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def split_section(
    text,
    source,
    section,
    section_title,
    start_chunk_id
):

    chunks = []

    step = (
        CHUNK_SIZE
        - OVERLAP
    )

    start = 0
    chunk_id = start_chunk_id

    while start < len(text):

        end = (
            start
            + CHUNK_SIZE
        )

        part = text[
            start:end
        ].strip()

        if part:

            chunks.append({
                "chunk_id": chunk_id,
                "source": source,
                "section": section,
                "section_title":
                    section_title,
                "text": part,

                # Heading is deliberately added
                # for better semantic retrieval
                "embedding_text":
                    (
                        f"Section {section}. "
                        f"{section_title}. "
                        f"{part}"
                    )
            })

            chunk_id += 1

        if end >= len(text):
            break

        start += step

    return chunks, chunk_id


def create_chunks(documents):

    chunks = []

    chunk_id = 1

    current_key = None
    section_paragraphs = []

    current_source = None
    current_section = None
    current_title = None


    def flush_section(
        paragraphs,
        source,
        section,
        title,
        next_id
    ):

        if not paragraphs:
            return [], next_id

        combined_text = " ".join(
            paragraphs
        )

        return split_section(
            combined_text,
            source,
            section,
            title,
            next_id
        )


    for record in documents:

        text = (
            record["text"]
            .strip()
        )

        if len(text) < 20:
            continue

        key = (
            record["source"],
            record["section"]
        )

        if (
            current_key is not None
            and key != current_key
        ):

            new_chunks, chunk_id = (
                flush_section(
                    section_paragraphs,
                    current_source,
                    current_section,
                    current_title,
                    chunk_id
                )
            )

            chunks.extend(
                new_chunks
            )

            section_paragraphs = []


        current_key = key

        current_source = (
            record["source"]
        )

        current_section = (
            record["section"]
        )

        current_title = (
            record["section_title"]
        )

        section_paragraphs.append(
            text
        )


    new_chunks, chunk_id = (
        flush_section(
            section_paragraphs,
            current_source,
            current_section,
            current_title,
            chunk_id
        )
    )

    chunks.extend(
        new_chunks
    )

    return chunks


documents = load_documents()

chunks = create_chunks(
    documents
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        chunks,
        file,
        indent=2,
        ensure_ascii=False
    )


print(
    "Paragraph records:",
    len(documents)
)

print(
    "Chunks created:",
    len(chunks)
)

print(
    "Saved to:",
    OUTPUT_FILE
)