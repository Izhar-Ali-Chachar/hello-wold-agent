from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17', google_api_key=os.getenv("GOOGLE_API_KEY"))

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    print(response.content)
    state['messages'].append(response)  # optional, if response is AIMessage or compatible
    return state

graph = StateGraph(AgentState)

graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

app = graph.compile()

user_input = input('Enter: ')
result = app.invoke({'messages': [HumanMessage(content=user_input)]})

print(result.content)
