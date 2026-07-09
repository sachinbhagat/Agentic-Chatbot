from src.agenticai.state.state import State

class BasicChatbotNode:
    def __init__(self, model):
        self.llm_model = model

    def process(self, state: State) -> dict:
        # Basic processing logic for the chatbot
        input_text = state["messages"][-1].content if state["messages"] else ""
        response = self.llm_model.invoke(input_text)
        return {"messages": [response]} 