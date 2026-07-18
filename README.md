# Recommendation Letter Generator RAG Model

A polished Streamlit app that uses retrieval-augmented generation to draft personalized academic letters of recommendation.

## Overview

This project analyzes student information, retrieves the closest matching recommendation-letter template with FAISS + sentence embeddings, and generates a tailored letter using Groq-hosted Llama models.

## Features

- Upload a student profile as a `.txt` file
- Score the profile using keyword and similarity signals
- Retrieve the most relevant LOR template with FAISS
- Generate a professional letter with Groq API
- Choose the recommendation strength before generating the final letter

## How it works

1. **Parse student information** from the uploaded text.
2. **Score the profile** using CGPA, achievements, skills, and research signals.
3. **Retrieve similar templates** using `all-MiniLM-L6-v2` embeddings and FAISS.
4. **Generate the final letter** with a level-based prompt.

## Project structure

- `main.py` - Streamlit UI and app flow
- `lor_indexer.py` - Template embedding and FAISS retrieval
- `lor_generator.py` - LOR generation via Groq API
- `sample_lor.json` - Example recommendation-letter templates
- `config.py` - Local API configuration

## Setup

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure your Groq API key

Set your key as an environment variable:

```bash
export GROQ_API_KEY="your_key_here"
```

On Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_key_here"
```

### 4) Run the app

```bash
streamlit run main.py
```

## Example input format

```text
Name: John Doe
CGPA: 3.92
Achievements: Dean's list, hackathon winner
Skills: Python, NLP, machine learning
Research: Undergraduate research assistant in AI
```

## Suggested improvements

- Move secrets out of source code and into environment variables
- Add loading and error states in the UI
- Add tests for scoring and level selection logic
- Improve template ranking by using cosine similarity
- Add export to PDF / DOCX for the generated letter
- Add a cleaner UI theme and sidebar layout

## Security note

Do not commit API keys to the repository. Rotate any exposed keys immediately and use environment variables or secret managers instead.

## License

Add a license file if you plan to share or reuse this project publicly.
