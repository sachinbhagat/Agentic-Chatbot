import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLMWrapper:
    def __init__(self, api_key: str, selected_model: str):
        self.api_key = api_key
        self.model = selected_model
        ## if api_key is not provided and env GROQ_API_KEY not available in os.environ, try to get it from environment variable  
        
        if not self.api_key:
            if "GROQ_API_KEY" in os.environ:
                self.api_key = os.environ["GROQ_API_KEY"]
                      
        self.llm = ChatGroq(api_key=self.api_key, model=self.model)

    def get_llm_model(self):
        return self.llm 




