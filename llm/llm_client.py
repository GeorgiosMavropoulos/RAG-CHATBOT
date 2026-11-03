"""This module calls initializes the LLM client"""
import os
from dotenv import load_dotenv
from google.genai import types
from google import genai
load_dotenv()
class LLM:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = os.getenv("GEMINI_MODEL")


    def get_llm(self,question)->str:

        """Call the LLM"""
        response = self.client.models.generate_content(
        model=self.model_name,
        contents=question,
       
        config=types.GenerateContentConfig(
            temperature=0.2 
        )
    )
        return response.text



