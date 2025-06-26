from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    skills: List[str]
    result: str

def first_node(state: AgentState) -> AgentState:

    state['result'] = f'{state["name"]}, welcome to the system '

    return state

def second_node(state: AgentState) -> AgentState:

    state['result'] = state['result'] + f'your are {state["age"]} old! '

    return state

# Third node: List the user's skills
def third_node(state: AgentState) -> AgentState:

    skill_list = ", ".join(state['skills'])  # Join the list into a string

    state['result'] += f'You have skills in: {skill_list}.'

    return state


graph = StateGraph(AgentState)

# Add nodes
graph.add_node('first_node', first_node)
graph.add_node('second_node', second_node)
graph.add_node('third_node', third_node)

# Connect the nodes in sequence
graph.add_edge('first_node', 'second_node')  # Fixed typo
graph.add_edge('second_node', 'third_node')

# Set the entry and finish points
graph.set_entry_point('first_node')
graph.set_finish_point('third_node')

app = graph.compile()

result = app.invoke({
    'name': 'izhat',
    'age': 20,
    'skills': ['ML', 'python developer', 'Generative Ai']
})

print(result)