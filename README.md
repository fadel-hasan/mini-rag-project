# mini-rag-project

mini-rag-project is a small FastAPI application for uploading files into project-specific folders.  
At the current stage, the project focuses on file upload handling, validation, and basic project directory management.

## Current Status

This project is still in an early stage and is not yet a full RAG system.  
It currently supports:

- uploading files through an API
- validating file type and size
- creating a folder for each project
- generating a unique file name for each uploaded file

## Requirements

- Python 3.10+
- pip

## Installation

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r src/requirements.txt
```
3. Create a `.env` file in the project root with the required settings:

```bash
cp .env.example .env
```

## Run the FastAPI server


```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

You can then access the API at:
```
http://0.0.0.0:5000
```

