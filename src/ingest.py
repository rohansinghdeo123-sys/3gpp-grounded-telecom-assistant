from pathlib import Path
from docx import Document
import json
import re


RAW_DIR = Path("data/raw")

OUTPUT_FILE = Path(
    "data/processed/documents.json"
)


HEADING_PATTERN = re.compile(
    r"^(\d+(?:\.\d+)*)\s+(.+)$"
)


def ingest_document(file_path):

    document = Document(file_path)

    records = []

    current_section = "Unknown"
    current_title = "Unknown"

    for paragraph in document.paragraphs:

        text = " ".join(
            paragraph.text.split()
        )

        if not text:
            continue

        style_name = (
            paragraph
            .style
            .name
            .lower()
        )

        # Ignore Word table-of-contents entries
        if style_name.startswith("toc"):
            continue

        if text.lower() == "contents":
            continue

        heading_match = (
            HEADING_PATTERN.match(text)
        )

        if (
            heading_match
            and (
                style_name.startswith("heading")
                or len(text) < 180
            )
        ):

            current_section = (
                heading_match.group(1)
            )

            current_title = (
                heading_match.group(2)
            )

            continue

        records.append({
            "source": file_path.name,
            "section": current_section,
            "section_title": current_title,
            "text": text
        })

    return records


def ingest_folder():

    all_records = []

    for file_path in RAW_DIR.glob(
        "*.docx"
    ):

        print(
            "Processing:",
            file_path.name
        )

        records = ingest_document(
            file_path
        )

        all_records.extend(
            records
        )

    return all_records


records = ingest_folder()


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        records,
        file,
        indent=2,
        ensure_ascii=False
    )


print(
    "Total cleaned records:",
    len(records)
)

print(
    "Saved to:",
    OUTPUT_FILE
)