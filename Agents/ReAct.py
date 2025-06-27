from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.prebuilt import ToolNode 
from langgraph.graph.message import add_messages 
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int) -> int:
    """This method is used to add two numbers"""
    return a + b

@tool
def multipy(a: int, b: int) -> int:
    """This method is used to multipy two numbers"""
    return a * b

tools = [add, multipy]

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17').bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    prompt = SystemMessage(content="You are my AI assistant, please answer my query to the best of your ability.")
    response = model.invoke([prompt] + state["messages"])
    return {"messages": state["messages"] + [response]}

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

graph = StateGraph(AgentState)
graph.add_node("model_call", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("model_call")
graph.add_edge("tools", "model_call")
graph.add_conditional_edges("model_call", should_continue, {"continue": "tools", "end": END})

app = graph.compile()

response = app.invoke({"messages": [HumanMessage(content="Add 40 + 12 and multipy 2 * 4 also in the last tell a me perfect joke.")]})
print(response)
