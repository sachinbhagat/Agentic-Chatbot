import streamlit as st
from collections.abc import Mapping
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class Message:
    def __init__(self, selected_usecase, graph, user_message):
        self.selected_usecase = selected_usecase
        self.graph = graph
        self.user_message = user_message

    @staticmethod
    def _extract_messages(state):
        if isinstance(state, Mapping):
            try:
                messages = state.get("messages")
                if messages is not None:
                    return messages
            except Exception:
                pass

        if hasattr(state, "get"):
            try:
                messages = state.get("messages")
                if messages is not None:
                    return messages
            except Exception:
                pass

        if hasattr(state, "messages"):
            return getattr(state, "messages")

        return []

    def display_result(self=None, selected_usecase=None, graph=None, user_message=None):
        if isinstance(self, Message):
            selected_usecase = self.selected_usecase if selected_usecase is None else selected_usecase
            graph = self.graph if graph is None else graph
            user_message = self.user_message if user_message is None else user_message
        elif selected_usecase is None or graph is None or user_message is None:
            raise TypeError("Message.display_result requires a Message instance or explicit arguments")

        st.write(f"User Message: {user_message}")
        st.write("Graph Result:")

        if selected_usecase == "Basic Chatbot":
            display_state = graph
            messages = []

            if hasattr(graph, "invoke") and callable(graph.invoke):
                try:
                    display_state = graph.invoke({"messages": [HumanMessage(content=user_message)]})
                except Exception as exc:
                    display_state = {"error": str(exc), "graph": repr(graph)}
            elif isinstance(graph, Mapping):
                try:
                    display_state = dict(graph)
                except TypeError:
                    display_state = graph
            else:
                display_state = graph

            if isinstance(display_state, Mapping):
                try:
                    messages = self._extract_messages(display_state)
                except TypeError:
                    messages = []
            else:
                messages = []

            st.json(display_state)

            if messages:
                for message in messages:
                    if isinstance(message, HumanMessage):
                        st.write(f"User: {message.content}")
                    elif isinstance(message, AIMessage):
                        st.write(f"AI: {message.content}")
                    elif isinstance(message, ToolMessage):
                        st.write(f"Tool: {message.content}")
            else:
                st.write("No messages found in the graph.")
