"""Streamlit UI for the AI code generator.  Run: streamlit run app.py"""
import streamlit as st

from codegen import extract_code_blocks, get_client, stream_code
from prompts import COMMENT_LEVELS, LANGUAGES, MODELS, TASKS

st.set_page_config(page_title="AI Code Generator", page_icon="💻", layout="wide")
st.title("💻 AI Code Generator")

if "history" not in st.session_state:
    st.session_state.history = []   # chat-style context for follow-ups
if "last_output" not in st.session_state:
    st.session_state.last_output = ""

# ---------------- Sidebar: API key + prompt parameters ----------------
with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("Anthropic API key", type="password",
                            help="Leave blank to use ANTHROPIC_API_KEY from your .env file")
    model = st.selectbox("Model", MODELS)

    st.header("⚙️ Prompt parameters")
    task = st.selectbox("Task", list(TASKS))
    language = st.selectbox("Language", list(LANGUAGES))
    framework = st.text_input("Framework / libraries (optional)", placeholder="e.g. FastAPI, React, pandas")
    style = st.selectbox("Code style", ["Clean & idiomatic", "Performance-focused", "Beginner-friendly", "Production-grade"])
    comments = st.select_slider("Comments", list(COMMENT_LEVELS), value="Moderate")
    explanation = st.radio("Explanation", ["None", "Short", "Detailed"], index=1, horizontal=True)
    type_hints = st.checkbox("Type hints", True)
    include_tests = st.checkbox("Include unit tests", False)
    error_handling = st.checkbox("Robust error handling", True)

    st.header("🎛️ Model settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05,
                            help="Lower = more deterministic code")
    max_tokens = st.slider("Max tokens", 256, 8000, 3000, 256)

    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.history = []
        st.session_state.last_output = ""
        st.rerun()

params = dict(model=model, task=task, language=language, framework=framework.strip(),
              style=style, comments=comments, explanation=explanation, type_hints=type_hints,
              include_tests=include_tests, error_handling=error_handling,
              temperature=temperature, max_tokens=max_tokens)

# ---------------- Main area ----------------
placeholder = {
    "Generate new code": "e.g. A REST API with endpoints to create, list and delete todo items",
    "Refactor existing code": "Paste the code to refactor here",
    "Debug / fix code": "Paste the buggy code and the error message here",
    "Write unit tests": "Paste the function/class to test here",
    "Explain code": "Paste the code to explain here",
    "Add docstrings & comments": "Paste the code here",
}[task]
request = st.text_area("Your request", height=200, placeholder=placeholder)

col1, col2 = st.columns([1, 5])
generate = col1.button("🚀 Generate", type="primary", use_container_width=True)

if generate:
    if not request.strip():
        st.warning("Please enter a request.")
    else:
        try:
            client = get_client(api_key or None)
            box, full = st.empty(), ""
            with st.spinner("Generating..."):
                for chunk in stream_code(client, request, params, st.session_state.history):
                    full += chunk
                    box.markdown(full + "▌")
            box.markdown(full)
            st.session_state.last_output = full
            st.session_state.history += [{"role": "user", "content": request},
                                         {"role": "assistant", "content": full}]
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- Output: code blocks + downloads ----------------
if st.session_state.last_output:
    blocks = extract_code_blocks(st.session_state.last_output)
    if blocks:
        st.divider()
        st.subheader("📦 Extracted code")
        ext = LANGUAGES[language]
        for i, (lang, code) in enumerate(blocks, 1):
            st.code(code, language=lang or language.lower())
            st.download_button(f"⬇️ Download block {i}", code,
                               file_name=f"generated_{i}.{ext}", key=f"dl_{i}")
    st.caption("Tip: write a follow-up request (e.g. “add logging”) and press Generate — context is kept until you start a new conversation.")
