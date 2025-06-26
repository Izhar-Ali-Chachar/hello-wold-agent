from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import random


class AgentState(TypedDict):
    name: str
    values: List[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    state['name'] = f"hy, {state['name']}"
    state['counter'] = 0
    return state


def random_node(state: AgentState) -> AgentState:
    state['values'].append(random.randint(0, 10))
    state['counter'] += 1
    return state


def should_continue(state: AgentState) -> str:
    if state['counter'] < 5:
        print(state['counter'])
        return 'loop'
    else:
        return 'exit'


# Build the graph
graph = StateGraph(AgentState)

graph.add_node('greeting_node', greeting_node)
graph.add_node('random_node', random_node)

graph.set_entry_point('greeting_node')  # Entry point
graph.add_edge('greeting_node', 'random_node')

graph.add_conditional_edges(
    'random_node',
    should_continue,
    {
        'loop': 'random_node',
        'exit': END
    }
)

# Compile the graph
app = graph.compile()

# Invoke with initial state
result = app.invoke({'name': 'izhar', 'values': [], 'counter': 0})

print(result)
