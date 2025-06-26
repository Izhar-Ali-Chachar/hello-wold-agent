from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    number1: int
    operator1: str
    number2: int
    number3: int
    operator2: str
    number4: int
    result1: str
    result2: str

def add_node1(state: AgentState) -> AgentState:

    state['result1'] = state['number1'] + state['number2']

    return state

def subtract_node1(state: AgentState) -> AgentState:

    state['result1'] = state['number1'] - state['number2']

    return state

def next_node_decide1(state: AgentState) -> AgentState:

    if state['operator1'] == '+':

        return 'addition_operation1'
    
    elif state['operator1'] == '-':

        return 'subtraction_operation1'
    

def add_node2(state: AgentState) -> AgentState:

    state['result2'] = state['number3'] + state['number4']

    return state

def subtract_node2(state: AgentState) -> AgentState:

    state['result2'] = state['number3'] - state['number4']

    return state

def next_node_decide2(state: AgentState) -> AgentState:

    if state['operator2'] == '+':

        return 'addition_operation2'
    
    elif state['operator2'] == '-':

        return 'subtraction_operation2'
    
graph = StateGraph(AgentState)

graph.add_node('add_node1', add_node1)
graph.add_node('subtract_node1', subtract_node1)
graph.add_node('add_node2', add_node2)
graph.add_node('subtract_node2', subtract_node2)
graph.add_node('route1', lambda state:state)
graph.add_node('route2', lambda state:state)

graph.add_edge(START, 'route1')

graph.add_conditional_edges(
    'route1',
    next_node_decide1,
    {
        'addition_operation1': 'add_node1',
        'subtraction_operation1': 'subtract_node1'
    }
)

graph.add_edge('add_node1', 'route2')
graph.add_edge('subtract_node1', 'route2')

graph.add_conditional_edges(
    'route2',
    next_node_decide2,
    {
        'addition_operation2': 'add_node2',
        'subtraction_operation2': 'subtract_node2'
    }
)

graph.add_edge('add_node2', END)
graph.add_edge('subtract_node2', END)

app = graph.compile()

result = app.invoke({'number1':30, 'operator1':'-', 'number2':20, 'number3':10, 'operator2':'+', 'number4':20})

print(result)