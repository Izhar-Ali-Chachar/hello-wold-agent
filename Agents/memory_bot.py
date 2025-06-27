from typing import TypedDict, List, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

def process(state: AgentState) -> AgentState:

    response = llm.invoke(state['messages'])

    print(response.content)

    state['messages'].append(AIMessage(content=response.content))

    print('current state: ', state['messages'])

    return state

graph = StateGraph(AgentState)

graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

app = graph.compile()


conversation_history = []

user_input = input("Enter: ")

while user_input != "exit":

    conversation_history.append(HumanMessage(content=user_input))

    result = app.invoke({"messages": conversation_history})

    conversation_history = result["messages"]

    user_input = input("Enter: ")


with open('logging_data', 'w') as file:

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f'AI: {message.content}\n')
    file.write('end of conversation')

print("Conversation saved to logging.txt")
