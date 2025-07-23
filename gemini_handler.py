# gemini_handler.py

import requests
import json
from config import GEMINI_API_KEY, MODEL_LLM, MODEL_API_URL
import google.generativeai as genai

class GeminiHandler:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(MODEL_LLM)

    def generate_llm_response(self, question):
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"[LỖI GEMINI LLM-only]: {e}"

    def generate_response_with_context(self, question, context):
        prompt = f"""Bạn là trợ lý pháp lý Việt Nam. Dưới đây là thông tin luật:

{context}

Câu hỏi của người dùng:
{question}

Trả lời:"""
        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            }
            res = requests.post(MODEL_API_URL, headers=headers, data=json.dumps(payload))
            if res.status_code == 200:
                result = res.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"[LỖI Gemini (Context)]: {res.status_code} - {res.text}"
        except Exception as e:
            return f"[LỖI Gemini Context]: {e}"
