\# 3GPP Grounded Telecom Assistant



A Retrieval-Augmented Generation (RAG) chatbot designed to answer telecom questions using \*\*official 3GPP standards documentation\*\* while minimizing unsupported or hallucinated responses.



\## Project Objective



The goal of this project is to build a telecom-focused conversational assistant that:



\* Uses official 3GPP documentation as its primary knowledge source

\* Retrieves relevant standards content before generating an answer

\* Rejects out-of-domain or weakly supported questions

\* Provides traceable source citations

\* Applies multiple validation layers to reduce hallucinations



\## Current Knowledge Scope



The current implementation is grounded on:



\*\*3GPP TS 23.501 — System Architecture for the 5G System (5GS)\*\*



Tested source file:



`23501-j40.docx`



The architecture supports ingestion of additional `.docx` specifications by placing them inside `data/raw/` and rebuilding the index.



Potential future additions include TS 23.502 and other relevant 3GPP specifications.



\## Architecture



```text

Official 3GPP Document

       ↓

Document Ingestion

      ↓

Cleaning + Section Metadata

       ↓

Section-Aware Chunking

       ↓

Sentence Transformer Embeddings

       ↓

Semantic Retrieval

       ↓

CrossEncoder Reranking

       ↓

Confidence Gate

       ↓

Strong Evidence?

   ┌───────┴───────┐

   No              Yes

   ↓                ↓

Abstain        Grounded LLM

                    ↓

                 Citations

                    ↓

                 Verifier

               ┌────┴────┐

              Fail      Pass

               ↓          ↓

           Abstain    Answer

```



\## Hallucination Reduction Strategy



The application does not rely only on prompt engineering.



Multiple safeguards are applied:



1\. \*\*Authoritative data source\*\* — answers are grounded in official 3GPP standards.

2\. \*\*Document cleaning\*\* — low-value structural content such as table-of-contents entries is removed.

3\. \*\*Section-aware chunking\*\* — unrelated specification sections are not mixed together.

4\. \*\*Semantic retrieval\*\* — relevant chunks are retrieved using dense embeddings.

5\. \*\*CrossEncoder reranking\*\* — retrieved candidates receive a stronger second-stage relevance check.

6\. \*\*Confidence gate\*\* — weak or out-of-domain retrieval results are rejected.

7\. \*\*Context-only generation\*\* — the LLM is explicitly instructed to answer only from retrieved evidence.

8\. \*\*Source citations\*\* — generated answers must reference supplied evidence.

9\. \*\*Answer verification\*\* — a separate verification stage checks whether generated claims are supported.

10\. \*\*Fail-closed abstention\*\* — if evidence or verification is insufficient, the assistant refuses to answer.



Example abstention:



> I could not find sufficient supporting information in the indexed 3GPP standards to answer this question.



\## Technology Stack



\* Python

\* Sentence Transformers

\* `all-MiniLM-L6-v2` embeddings

\* CrossEncoder reranking

\* NumPy

\* Groq LLM API

\* Streamlit

\* python-docx

\* python-dotenv



\## Project Structure



```text

3gpp-rag-chatbot/

├── data/

│   ├── raw/

│   └── processed/

├── indexes/

├── src/

│   ├── config.py

│   ├── ingest.py

│   ├── chunker.py

│   ├── embedder.py

│   ├── retriever.py

│   ├── reranker.py

│   ├── generator.py

│   ├── verifier.py

│   └── pipeline.py

├── app.py

├── evaluate.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Pipeline Components



\### `ingest.py`



Reads the source 3GPP Word document, cleans structural noise, extracts textual content, and preserves metadata such as source specification, section number, and section title.



\### `chunker.py`



Groups related content by section and creates overlapping chunks suitable for semantic retrieval.



\### `embedder.py`



Converts cleaned chunks into dense semantic embeddings using Sentence Transformers and persists the embedding matrix locally.



\### `retriever.py`



Embeds the user query and performs semantic similarity ranking against the stored chunk embeddings.



\### `reranker.py`



Uses a CrossEncoder to re-evaluate the retrieved question-passage pairs and retain the strongest evidence.



\### `generator.py`



Provides only approved 3GPP evidence to the LLM and requires grounded answers with citations.



\### `verifier.py`



Validates citations and checks whether the generated answer is supported by the provided evidence.



\### `pipeline.py`



Orchestrates retrieval, reranking, confidence gating, generation, and verification.



\### `evaluate.py`



Evaluates the confidence gate using both supported telecom questions and deliberately unsupported questions.



\### `app.py`



Provides the final Streamlit conversational interface.



\## Setup



\### 1. Clone the repository



```bash

git clone <repository-url>

cd 3gpp-rag-chatbot

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



On Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Add the 3GPP specification



Download the required specification from the official 3GPP standards archive.



Place the `.docx` file inside:



```text

data/raw/

```



The current implementation was tested using:



```text

23501-j40.docx

```



\### 5. Create `.env`



```text

GROQ\_API\_KEY=YOUR\_GROQ\_API\_KEY



GROQ\_MODEL=llama-3.3-70b-versatile



EMBEDDING\_MODEL=sentence-transformers/all-MiniLM-L6-v2



RERANKER\_MODEL=cross-encoder/ms-marco-MiniLM-L6-v2



SEMANTIC\_TOP\_K=12



FINAL\_TOP\_K=4



MIN\_SEMANTIC\_SCORE=0.25



MIN\_RERANK\_SCORE=0.60

```



The `.env` file is intentionally excluded from version control.



\## Build the Knowledge Base



Run the pipeline in order:



```bash

python src/ingest.py

python src/chunker.py

python -m src.embedder

```



\## Evaluate Retrieval Confidence



```bash

python evaluate.py

```



The evaluation contains both supported 3GPP queries and unrelated queries to validate the abstention mechanism.



\## Run the Application



```bash

streamlit run app.py

```



Open:



```text

http://localhost:8501

```



\## Example Supported Questions



\* What is the role of the Access and Mobility Management Function?

\* What does the Session Management Function do?

\* What is the purpose of the User Plane Function?

\* What is UDM?

\* What is the role of PCF?



\## Out-of-Domain Test



Example:



> Who won the FIFA World Cup in 2022?



Expected behavior:



> I could not find sufficient supporting information in the indexed 3GPP standards to answer this question.



The system deliberately avoids answering from the LLM's general knowledge when sufficient 3GPP evidence is unavailable.



\## Design Decision: Why RAG?



3GPP specifications are external knowledge sources that can evolve between releases.



RAG allows the knowledge base to be updated independently from the LLM while also providing:



\* Source traceability

\* Better factual grounding

\* Easier document updates

\* Explicit evidence inspection

\* Better control over unsupported answers



\## Limitations



\* Current knowledge coverage is limited primarily to TS 23.501.

\* Confidence thresholds are application-specific and should be calibrated on a larger evaluation dataset.

\* Retrieval quality depends on document structure, chunking, and embedding quality.

\* LLM verification reduces risk but does not mathematically guarantee zero hallucination.



\## Future Improvements



\* Add TS 23.502 and additional 3GPP specifications

\* Larger automated evaluation benchmark

\* Hybrid semantic + lexical retrieval

\* Release-aware specification filtering

\* Improved section-level citations

\* Retrieval and response latency monitoring

\* Containerized deployment



\## Disclaimer



This project is an educational/recruitment implementation demonstrating grounded Retrieval-Augmented Generation over telecom standards. It is not an official 3GPP product or standards interpretation service.



