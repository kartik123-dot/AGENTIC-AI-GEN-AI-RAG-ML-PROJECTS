import streamlit as st
import ollama

# Initialize the Ollama client
client = ollama.Client(host="http://localhost:8501")

st.set_page_config(
    page_title="Ollama Streamlit App made by Kartik Soni",
    layout="wide"
)

st.title("Mr.Kartik Soni - Ollama Streamlit App")

prompt = st.text_area("Enter your prompt:", height=200)

if st.button("Generate Response"):
    if prompt.strip()=="deepseek-r1:1.5b":
        st.warning("Please Enter a prompt")
    else:
        with st.spinner("Thinking..."):
            response = client.generate(
                model="deepseek-r1:1.5b",
                message = [
                    {"role": "user", "content": prompt}
                ]
            )

            st.success("Response Generated!")
            st.write(response["message"]["content"])