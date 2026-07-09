from configparser import ConfigParser

class ConfigFile:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config = ConfigParser()
        self.config.read(self.config_file_path)

    def get_page_title(self):
        return self.config.get('default', 'PAGE_TITLE', fallback='LangGraph: An Agentic AI for Knowledge Graphs')

    def get_llm_options(self):
        llm_options = self.config.get('default', 'LLM_OPTIONS', fallback='Groq')
        return [option.strip() for option in llm_options.split(',')]

    def get_usecase_options(self):
        usecase_options = self.config.get('default', 'USECASE_OPTIONS', fallback='Basic Chatbot')
        return [option.strip() for option in usecase_options.split(',')]

    def get_model_options(self):
        model_options = self.config.get('default', 'MODEL_OPTIONS', fallback='llama3-8b-8192, llama3-70b-8192, gemma2-9b-it')
        return [option.strip() for option in model_options.split(',')]