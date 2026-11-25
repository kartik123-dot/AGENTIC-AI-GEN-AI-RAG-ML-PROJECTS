# AI Code Generator (Streamlit + Anthropic API)

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then paste your API key into .env
streamlit run app.py
```
Opens at http://localhost:8501. You can also paste the key in the sidebar instead of using `.env`.

## Files
- `app.py`      – Streamlit UI (sidebar parameters, streaming output, downloads)
- `codegen.py`  – API client, streaming, code-block extraction
- `prompts.py`  – prompt templates + parameter options (edit to customise)
