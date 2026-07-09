from langgraph.graph import StateGraph, START, END
from src.agenticai.state.state import State
from src.agenticai.nodes.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, model):
        self.llm_model = model
        self.graph_builder = StateGraph(State)

    def build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm_model)
        # Add the LLM model to the graph
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        return self.graph_builder.compile()  # Compile the graph before returning