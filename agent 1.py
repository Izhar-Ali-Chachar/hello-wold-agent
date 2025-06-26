from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

def greetrings(state: AgentState) -> AgentState:

    state['message'] = f'hey {state["message"]} how are you?'

    return state

graph = StateGraph(AgentState)

graph.add_node('greeter', greetrings)

graph.set_entry_point('greeter')
graph.set_finish_point('greeter')

app = graph.compile()

print(app.invoke({'message': 'bob'}))