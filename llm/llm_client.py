"""This module calls initializes the LLM client"""
import os
from dotenv import load_dotenv
from google.genai import types
from google import genai

from google.api_core import exceptions as google_exceptions
import requests
load_dotenv()
class LLM:
    def __init__(self):
      try:
        self.client = genai.Client()
        self.model_name = os.getenv("GEMINI_MODEL")
        if not self.model_name:
                raise ValueError("Model name has not been declared")

      except ValueError as e:
        print(f'Configuration error: {e}')
        raise e

      except google_exceptions.GoogleAPICallError as e:
            print(f"Error during API connection with LLM: {e}")
            raise RuntimeError("Failed to connect with the LLM") from e

      except Exception as e:
            print(f"An unexpected error occured during connection: {e}")
            raise e


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



