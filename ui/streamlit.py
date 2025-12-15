import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Bank Annual Report RAG", layout="wide")
st.title("Bank Annual Report RAG")

# Controls
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    question = st.text_input("Question", value="What are the main risk factors mentioned for 2024?")
with col2:
    bank = st.selectbox("Bank", ["TD"], index=0)
with col3:
    year = st.selectbox("Year", [2024], index=0)

k = st.slider("Top-k chunks", min_value=1, max_value=10, value=5)

ask_btn = st.button("Ask")

if ask_btn:
    if not question.strip():
        st.warning("Please type a question.")
        st.stop()

    payload = {"question": question, "bank": bank, "year": int(year), "k": int(k)}

    with st.spinner("Thinking..."):
        try:
            r = requests.post(API_URL, json=payload, timeout=120)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    # Show answer
    st.subheader("Answer")
    st.write(data.get("answer", ""))

    # Show sources
    st.subheader("Sources")
    sources = data.get("sources", [])
    if not sources:
        st.info("No sources returned.")
    else:
        for i, s in enumerate(sources, 1):
            st.markdown(f"**{i}. page {s.get('pdf_page')} | chunk {s.get('chunk_id')}**")
            snippet = s.get("snippet")
            if snippet:
                st.code(snippet)
