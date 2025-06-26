from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    number1: int
    operator: str
    number2: int
    result: str

def add_node(state: AgentState) -> AgentState:

    state['result'] = state['number1'] + state['number2']

    return state

def subtract_node(state: AgentState) -> AgentState:

    state['result'] = state['number1'] - state['number2']

    return state

def next_node_decide(state: AgentState) -> AgentState:

    if state['operator'] == '+':

        return 'addition_operation'
    
    elif state['operator'] == '-':

        return 'subtraction_operation'
    
graph = StateGraph(AgentState)

graph.add_node('add_node', add_node)
graph.add_node('subtract_node', subtract_node)
graph.add_node('route', lambda state:state)

graph.add_edge(START, 'route')

graph.add_conditional_edges(
    'route',
    next_node_decide,
    {
        'addition_operation': 'add_node',
        'subtraction_operation': 'subtract_node'
    }
)

graph.add_edge('add_node', END)
graph.add_edge('subtract_node', END)

app = graph.compile()

result = app.invoke({'number1':10, 'operator':'+', 'number2':20})

print(result)