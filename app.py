import streamlit as st
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from neo4j_handler import Neo4jHandler
from gemini_handler import GeminiHandler

# Cấu hình giao diện
st.set_page_config(page_title="Trợ lý Pháp lý Việt Nam", layout="wide")
st.title("⚖️ Trợ lý Pháp lý Việt Nam")

# Khởi tạo mỗi lần chạy (không dùng cache)
neo4j = Neo4jHandler(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
gemini = GeminiHandler()

# Nhập câu hỏi
user_input = st.text_input("📌 Hãy nhập câu hỏi liên quan đến pháp luật:")

if user_input:
    # Kết quả từ Neo4j
    with st.expander("📚 Kết quả từ Neo4j (tri thức luật):", expanded=True):
        neo4j_context = neo4j.get_context_from_law(user_input)
        st.write(neo4j_context)

    # Kết quả từ LLM-only
    with st.expander("🤖 Kết quả từ Gemini (LLM-only):", expanded=False):
        llm_response = gemini.generate_llm_response(user_input)
        st.write(llm_response)

    # Kết quả từ KG + LLM
    with st.expander("🧠 Kết hợp Neo4j + Gemini (KG + LLM):", expanded=False):
        full_response = gemini.generate_response_with_context(user_input, neo4j_context)
        st.write(full_response)

# Đóng kết nối (optional, nhưng nên để)
if 'neo4j' in locals():
    neo4j.close()
