import streamlit as st
import requests

st.title("🧠 RAG Chatbot (Streamlit UI)")

query = st.text_input("Ask your question:")

if st.button("Submit"):
    if query:
        response = requests.post("http://localhost:8000/ask", json={"question": query})
        if response.status_code == 200:
            answer = response.json()['answer']
            st.markdown(f"**Answer:**\n\n{answer}")
        else:
            st.error("Error from backend")
    else:
        st.warning("Please enter a question.")
