from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str

def reply_node(state: AgentState) -> AgentState:

    state['name'] = f'{state['name']}, you are doing great in learning'

    return state

graph = StateGraph(AgentState)

graph.add_node('edge', reply_node)

graph.set_entry_point('edge')
graph.set_finish_point('edge')

app = graph.compile()

print(app.invoke({'name': 'izhar'}))