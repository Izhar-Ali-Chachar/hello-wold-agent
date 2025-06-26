from langgraph.graph import StateGraph
from typing import TypedDict, List

# Define the shape of the data
class AgentState(TypedDict):
    name: str
    operation: str
    values: List[int]
    result: str

# Function that processes the input
def process_values(state: AgentState) -> AgentState:
    op = state['operation']
    values = state['values']

    # Perform the operation
    if op == '*':
        result = 1
        for i in values:
            result *= i
    elif op == '+':
        result = sum(values)
    elif op == '/':
        result = values[0]
        for v in values[1:]:
            result /= v
    else:
        result = 'Unsupported operation'
        state['result'] = f"hey {state['name']}, the operation '{op}' is not supported."
        return state

    # Add result message to the state
    state['result'] = f"hey {state['name']}, your calculation equals = {result}"

    return state

# Create the graph
graph = StateGraph(AgentState)
graph.add_node('edge', process_values)
graph.set_entry_point('edge')
graph.set_finish_point('edge')

# Compile and invoke
app = graph.compile()

# Run it
print(app.invoke({'name': 'izhar', 'operation': '%', 'values': [1, 2, 3, 4], 'result': ''}))
