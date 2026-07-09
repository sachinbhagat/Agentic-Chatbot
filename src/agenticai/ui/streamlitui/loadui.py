import streamlit as st
import os 
from src.agenticai.ui.configfile import ConfigFile

class LoadUI:
    def __init__(self, config_file_path):
        self.config = ConfigFile(config_file_path)

    def load_ui(self):
        st.set_page_config(page_title=self.config.get_page_title())
        st.title(self.config.get_page_title())
        
        with st.sidebar:           
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            model_options = self.config.get_model_options()

            selected_llm = st.selectbox("Select LLM", llm_options)
            selected_usecase = st.selectbox("Select Use Case", usecase_options)
            selected_model = st.selectbox("Select Model", model_options) 
            api_key = os.environ["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Enter your API Key", type="password")
                        
            # Validate API key
            if not api_key:
                st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
        
        return selected_llm, selected_usecase, selected_model, api_key