"""This module calls initializes the LLM client"""
import os
from dotenv import load_dotenv
from google.genai import types
from google import genai
import requests
load_dotenv()
class LLM:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = os.getenv("GEMINI_MODEL")


    def get_llm(self,question)->str:
      try:
        """Call the LLM"""
        response = self.client.models.generate_content(
        model=self.model_name,
        contents=question,
       
        config=types.GenerateContentConfig(
            temperature=0.2 
        )
    )
        return response.text

      except requests.exceptions.RequestException as e:
       raise RuntimeError("The LLM is unavailable") from e
      except Exception as e:
         raise RuntimeError(f"An unexpected error occurred: {e}") from e



