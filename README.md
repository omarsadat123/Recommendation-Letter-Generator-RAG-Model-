# Recommendation Letter Generator (RAG)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/ui-streamlit-red)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A Retrieval-Augmented Generation (RAG) application that analyzes student profiles, matches them to reference recommendation templates using FAISS similarity search, and generates tailored letters via the Groq API.

## Features

- Streamlit UI for uploading student profile text
- FAISS + sentence-transformers template retrieval
- Rule-based scoring and recommendation-level prediction
- Groq-backed LOR generation by level
- Environment-based configuration for secure API setup

## Project Structure

```text
.
├── src/lor_rag/
│   ├── app.py          # Streamlit app and scoring logic
│   ├── config.py       # Environment-based settings
│   ├── generator.py    # Groq API integration
│   └── indexer.py      # FAISS template indexing/search
├── sample_lor.json     # Reference template data
├── lor_index.faiss     # Serialized FAISS index
├── tests/
├── requirements.txt
└── setup.py
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file from `.env.example` and set your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Optional:

- `APP_ENV` (default: `development`)
- `GROQ_API_URL` (default: Groq chat completions URL)
- `LOR_MODEL_NAME` (default: `llama3-70b-8192`)

## Usage

```bash
streamlit run /home/runner/work/Recommendation-Letter-Generator-RAG-Model-/Recommendation-Letter-Generator-RAG-Model-/main.py
```

Upload a `.txt` student profile and generate an LOR based on predicted or selected recommendation strength.

## API / Module Documentation

### `lor_rag.app`
- `extract_score(text: str) -> int`: Heuristic profile scoring (1-10).
- `lor_level(rating: int) -> str`: Maps rating to recommendation band.
- `main() -> None`: Streamlit application entrypoint.

### `lor_rag.indexer`
- `LORIndexer.create_index() -> None`: Builds FAISS index from templates.
- `LORIndexer.search_match(input_text: str) -> tuple[int, int]`: Returns match index and normalized similarity score.

### `lor_rag.generator`
- `LORGenerator.generate_lor(user_text: str, lor_level: str) -> str`: Calls Groq API and returns generated LOR text.

## Example Template Data Schema

`sample_lor.json` entries follow:

```json
{
  "type": "academic",
  "level": "high",
  "template": "...letter template text..."
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
