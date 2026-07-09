import streamlit as st
from src.agenticai.ui.streamlitui.loadui import LoadUI
from src.agenticai.LLMS.groqllm import GroqLLMWrapper
from src.agenticai.graph.graph_builder import GraphBuilder
from src.agenticai.ui.streamlitui.display_result import Message

def main_app():
    config_file_path = "/src/agenticai/ui/configfile.ini"  # Path to your configuration file
    ui = LoadUI(config_file_path)
    selected_llm, selected_usecase, selected_model, api_key = ui.load_ui()

    # You can now use the selected options and API key in your application logic
     
    
    user_message = st.chat_input("Enter your message here...")  # Example chat input field

    if user_message:
        try:           
            llm_wrapper = GroqLLMWrapper(api_key=api_key, selected_model=selected_model)
            llm_model = llm_wrapper.get_llm_model()

            if not llm_model:
                st.error("Failed to initialize the LLM model. Please check your API key and model selection.")  
                return
           
            if not selected_usecase:
                st.error("No use case selected. Please select a use case from the sidebar.")
                return  # Exit the function if no use case is selected

            if selected_usecase == "Basic Chatbot":
                # Here you can implement the logic for the basic chatbot use case
                # For example, you can call a function that handles the chatbot interaction
                st.write("Basic Chatbot is selected. Implement the chatbot logic here.")
                graph_builder = GraphBuilder(llm_model)                
                state_graph = graph_builder.build_graph()                
                Message(selected_usecase, state_graph, user_message).display_result()               
        
        except Exception as e:
            st.error(f"Failed to process the request: {str(e)}")
            return  # Exit the function if there's an error initializing the model
        