# main.py

from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from neo4j_handler import Neo4jHandler
from gemini_handler import GeminiHandler

def main():
    neo4j = Neo4jHandler(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    gemini = GeminiHandler()

    print("Chào bạn! Tôi là trợ lý luật pháp Việt Nam. Hãy hỏi tôi về điều luật, tội phạm, hình phạt,...")
    print("Gõ 'thoát' để kết thúc.\n")

    while True:
        user_input = input("Bạn: ")
        if user_input.lower().strip() == "thoát":
            break

        # Neo4j context
        neo4j_context = neo4j.get_context_from_law(user_input)
        print("\n[NEO4J]:")
        print(neo4j_context)

        # Gemini: LLM-only
        print("\n[LLM GEMINI - Chỉ dùng câu hỏi]:")
        print(gemini.generate_llm_response(user_input))

        # Gemini: Với ngữ cảnh từ Neo4j
        print("\n[KG + LLM - Dùng dữ liệu từ Neo4j]:")
        print(gemini.generate_response_with_context(user_input, neo4j_context))
        print("\n" + "-"*60)

    neo4j.close()
    print("Tạm biệt!")

if __name__ == "__main__":
    main()
