# from neo4j_handler import Neo4jHandler
# from gemini_handler import GeminiHandler
# import re

# class ChatbotLogic:
#     def __init__(self, neo4j_handler: Neo4jHandler, gemini_handler: GeminiHandler):
#         self.neo4j_handler = neo4j_handler
#         self.gemini_handler = gemini_handler

#     def query_neo4j_for_context(self, user_question):
#         context = []
#         lower_question = user_question.lower()

#         # Trường hợp 1: Hỏi về điều luật cụ thể
#         match = re.search(r"\b(điều|Điều)\s*(\d{1,3})\b", user_question)
#         if match:
#             so_dieu = f"Điều {match.group(2)}"
#             query = """
#             MATCH (d:Dieu_Luat)
#             WHERE d.name STARTS WITH $so_dieu
#             OPTIONAL MATCH (d)-[:QUY_ĐỊNH_HÀNH_VI]->(hv:Hanh_Vi)
#             RETURN d.name AS name, d.content AS content, collect(hv.name) AS hanh_vis
#             LIMIT 1
#             """
#             results = self.neo4j_handler.execute_query(query, {"so_dieu": so_dieu})
#             if results:
#                 res = results[0]
#                 context.append(f"**{res['name']}**: {res['content']}")
#                 if res['hanh_vis']:
#                     context.append("**Hành vi liên quan:**")
#                     for hv in res['hanh_vis']:
#                         if hv:
#                             context.append(f"- {hv}")
#             else:
#                 context.append(f"Không tìm thấy nội dung cho {so_dieu} trong bộ luật.")

#         # Trường hợp 2: Tìm điều luật từ hành vi
#         elif any(keyword in lower_question for keyword in ["bị xử lý", "nằm trong điều", "áp dụng", "điều nào xử lý"]):
#             keyword_match = re.search(r"tội\s+(.*?)\b|hành vi\s+(.*?)\b", lower_question)
#             if keyword_match:
#                 keyword = keyword_match.group(1) or keyword_match.group(2)
#                 query = """
#                 MATCH (hv:Hanh_Vi)
#                 WHERE toLower(hv.name) CONTAINS $keyword
#                 MATCH (d:Dieu_Luat)-[:QUY_ĐỊNH_HÀNH_VI]->(hv)
#                 RETURN d.name AS dieu, d.content AS content
#                 LIMIT 1
#                 """
#                 results = self.neo4j_handler.execute_query(query, {"keyword": keyword})
#                 if results:
#                     res = results[0]
#                     context.append(f"Hành vi '{keyword}' được quy định trong {res['dieu']}: {res['content']}")
#                 else:
#                     context.append(f"Không tìm thấy điều luật nào quy định cho hành vi '{keyword}'.")

#         # Trường hợp 3: Hỏi về hành vi phạm tội
#         elif any(keyword in lower_question for keyword in ["tội", "phạm tội", "hành vi"]):
#             query = """
#             MATCH (hv:Hanh_Vi)
#             RETURN hv.name AS name, hv.content AS content
#             LIMIT 5
#             """
#             results = self.neo4j_handler.execute_query(query)
#             if results:
#                 context.append("Một số hành vi phạm tội trong luật hình sự:")
#                 for res in results:
#                     if res['name']:
#                         if res.get('content'):
#                             context.append(f"- {res['name']}: {res['content']}")
#                         else:
#                             context.append(f"- {res['name']}")
#             else:
#                 context.append("Không tìm thấy thông tin về hành vi phạm tội.")

#         # Trường hợp 4: Hỏi về hình phạt nặng
#         elif any(x in lower_question for x in ["tử hình", "chung thân", "mức án cao"]):
#             query = """
#             MATCH (hp:Hinh_Phat)
#             WHERE toLower(hp.name) CONTAINS 'tử hình' OR toLower(hp.name) CONTAINS 'chung thân'
#             OPTIONAL MATCH (hv:Hanh_Vi)-[:BỊ_XỬ_PHẠT_BỞI]->(hp)
#             RETURN hp.name AS hinh_phat, collect(hv.name) AS hanh_vis
#             """
#             results = self.neo4j_handler.execute_query(query)
#             if results:
#                 for res in results:
#                     context.append(f"**Hình phạt:** {res['hinh_phat']}")
#                     context.append("Áp dụng cho các hành vi:")
#                     for hv in res['hanh_vis']:
#                         if hv:
#                             context.append(f"- {hv}")
#             else:
#                 context.append("Không tìm thấy thông tin về hình phạt nặng.")

#         # Trường hợp 5: Hình phạt nói chung
#         elif "hình phạt" in lower_question or "xử lý" in lower_question:
#             query = """
#             MATCH (hp:Hinh_Phat)
#             RETURN hp.name AS name, hp.content AS content
#             LIMIT 5
#             """
#             results = self.neo4j_handler.execute_query(query)
#             if results:
#                 context.append("Một số hình phạt trong luật hình sự:")
#                 for res in results:
#                     if res['name']:
#                         if res.get('content'):
#                             context.append(f"- {res['name']}: {res['content']}")
#                         else:
#                             context.append(f"- {res['name']}")
#             else:
#                 context.append("Không tìm thấy thông tin về hình phạt.")

#         if not context:
#             context.append("Xin lỗi, tôi chưa tìm thấy thông tin phù hợp trong đồ thị. Bạn có thể thử hỏi về một điều luật cụ thể như 'Điều 173', hoặc hỏi về 'tội danh', 'hành vi', hoặc 'hình phạt'.")

#         return "\n".join(context)

#     def chat(self, question):
#         context = self.query_neo4j_for_context(question)

#         print("\n--- Ngữ cảnh từ Đồ thị Luật Hình Sự ---")
#         print(context)
#         print("----------------------------------\n")

#         # So sánh giữa Gemini và dữ liệu Neo4j (cho mục đích nghiên cứu)
#         try:
#             gemini_response = self.gemini_handler.generate_response(question, context)
#         except Exception as e:
#             gemini_response = f"[LỖI GEMINI]: {str(e)}"

#         return f"[NEO4J]:\n{context}\n\n[LLM GEMINI]:\n{gemini_response}"