import streamlit as st
import requests

st.title("🧠 RAG Chatbot (Streamlit UI)")

query = st.text_input("Ask your question:")

if st.button("Submit"):
    if query:
        response = requests.post("http://localhost:8000/ask", json={"question": query})
        if response.status_code == 200:
            result = response.json()

            # ✅ Show the Answer
            st.markdown("### ✅ Answer")
            st.write(result["answer"])

            # ✅ Show Source File Links
            st.markdown("### 📄 Source Documents")
            unique_filenames = set()
            for source in result.get("sources", []):
                filename = source["filename"]
                if filename not in unique_filenames:
                    unique_filenames.add(filename)
                    download_url = f"http://localhost:8000/download/{filename}"
                    st.markdown(f'<a href="{download_url}" target="_blank">📄 Open `{filename}` in new tab</a>', unsafe_allow_html=True)
        else:
            st.error("❌ Error from backend!")
    else:
        st.warning("Please enter a question.")
