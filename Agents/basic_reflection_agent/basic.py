from langgraph.graph import MessageGraph, END, START
from langchain_core.messages import HumanMessage, BaseMessage
from chains import generative_chain, critiqe_chain
from dotenv import load_dotenv

load_dotenv()

def generative_node(state: list[BaseMessage]) -> list[BaseMessage]:
    response = generative_chain.invoke({'messages': state})
    return state + [response]

def critiqe_node(state: list[BaseMessage]) -> list[BaseMessage]:
    response = critiqe_chain.invoke({'messages': state})
    return state + [HumanMessage(content=response.content)]

def should_continue(state: list[BaseMessage]) -> str:
    if len(state) < 5:
        return 'reflect'
    else:
         return END

graph = MessageGraph()

graph.add_node('generate', generative_node)
graph.add_node('reflect', critiqe_node)

graph.add_edge(START, 'generate')
graph.add_conditional_edges('generate', should_continue, {'reflect': 'reflect', END: END})
graph.add_edge('reflect', 'generate')  # fixed


app = graph.compile()

response = app.invoke(HumanMessage(content='ai agents takeing over content creation'))
print(response)