import sys
import types
import unittest
from collections.abc import Mapping
from unittest.mock import patch

streamlit_stub = types.ModuleType("streamlit")
streamlit_stub.subheader = lambda *args, **kwargs: None
streamlit_stub.write = lambda *args, **kwargs: None
streamlit_stub.json = lambda *args, **kwargs: None
sys.modules.setdefault("streamlit", streamlit_stub)

messages_module = types.ModuleType("langchain_core.messages")


class HumanMessage:
    def __init__(self, content=""):
        self.content = content


class AIMessage:
    def __init__(self, content=""):
        self.content = content


class ToolMessage:
    def __init__(self, content=""):
        self.content = content


messages_module.HumanMessage = HumanMessage
messages_module.AIMessage = AIMessage
messages_module.ToolMessage = ToolMessage
sys.modules.setdefault("langchain_core", types.ModuleType("langchain_core"))
sys.modules.setdefault("langchain_core.messages", messages_module)
sys.modules["langchain_core"].messages = messages_module

from src.agenticai.ui.streamlitui.display_result import Message


class CompiledGraphStub:
    def __repr__(self):
        return "CompiledStateGraph"


class InvokableGraphStub:
    def invoke(self, state):
        return {"messages": [HumanMessage("Hello from graph"), AIMessage("Hi there")]}


class DictLikeGraphStub(dict):
    def __contains__(self, item):
        raise TypeError("argument of type 'CompiledStateGraph' is not iterable")


class MappingLikeGraphStub(Mapping):
    def __init__(self, messages=None):
        self._messages = messages or []

    def __getitem__(self, key):
        raise KeyError(key)

    def __iter__(self):
        raise TypeError("argument of type 'CompiledStateGraph' is not iterable")

    def __len__(self):
        return 0


class MessageDisplayResultTests(unittest.TestCase):
    def test_display_result_uses_instance_state(self):
        with patch("src.agenticai.ui.streamlitui.display_result.st.subheader") as subheader_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.write") as write_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.json") as json_mock:
            message = Message("Basic Chatbot", {"messages": []}, "Hello")

            message.display_result()

            write_mock.assert_any_call("User Message: Hello")
            write_mock.assert_any_call("No messages found in the graph.")
            json_mock.assert_called_once_with({"messages": []})

    def test_display_result_handles_compiled_graph_objects(self):
        with patch("src.agenticai.ui.streamlitui.display_result.st.subheader") as subheader_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.write") as write_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.json") as json_mock:
            message = Message("Basic Chatbot", CompiledGraphStub(), "Hello")

            message.display_result()

            write_mock.assert_any_call("User Message: Hello")
            write_mock.assert_any_call("No messages found in the graph.")
            json_mock.assert_called_once_with(message.graph)

    def test_display_result_invokes_graph_objects(self):
        with patch("src.agenticai.ui.streamlitui.display_result.st.write") as write_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.json") as json_mock:
            message = Message("Basic Chatbot", InvokableGraphStub(), "Hello")

            message.display_result()

            write_mock.assert_any_call("User: Hello from graph")
            write_mock.assert_any_call("AI: Hi there")
            self.assertEqual(json_mock.call_count, 1)
            state = json_mock.call_args[0][0]
            self.assertIn("messages", state)
            self.assertEqual(len(state["messages"]), 2)
            self.assertEqual(state["messages"][0].content, "Hello from graph")
            self.assertEqual(state["messages"][1].content, "Hi there")

    def test_display_result_handles_mapping_like_graphs_without_membership_errors(self):
        with patch("src.agenticai.ui.streamlitui.display_result.st.write") as write_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.json") as json_mock:
            message = Message("Basic Chatbot", DictLikeGraphStub(messages=[]), "Hello")

            message.display_result()

            write_mock.assert_any_call("User Message: Hello")
            write_mock.assert_any_call("No messages found in the graph.")
            json_mock.assert_called_once_with(message.graph)

    def test_display_result_handles_mapping_like_graphs_that_raise_on_iteration(self):
        with patch("src.agenticai.ui.streamlitui.display_result.st.write") as write_mock, \
             patch("src.agenticai.ui.streamlitui.display_result.st.json") as json_mock:
            message = Message("Basic Chatbot", MappingLikeGraphStub(messages=[]), "Hello")

            message.display_result()

            write_mock.assert_any_call("User Message: Hello")
            write_mock.assert_any_call("No messages found in the graph.")
            json_mock.assert_called_once_with(message.graph)


if __name__ == "__main__":
    unittest.main()
