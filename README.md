# ai-engineer-project-2-prompting-safety

## Overview

This project demonstrates safe, schema-validated LLM prompting. Day 8 focuses on forcing valid JSON output from an LLM, parsing, and validating it against a strict schema. This is the foundation for secure, moderated summarization in later capstones.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
4. Set your OpenAI API key in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

**Do not commit your `.env` file to version control.**

## How to run

```bash
source .venv/bin/activate
python -m src.day_08.day_08_json_generator
```

## Project Structure

- `src/p2/json_utils.py`: JSON schema and validation
- `src/day_08/day_08_json_generator.py`: JSON-forced LLM call and validation
