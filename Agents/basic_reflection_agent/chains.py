from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# Generation prompt
gen_prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        "You are a Twitter tech influencer assistant tasked with writing excellent Twitter posts. "
        "Generate the best Twitter post based on the user's prompt. "
        "If the user provides a critique, respond with an updated version of the previous one."
    ),
    MessagesPlaceholder(variable_name='messages')
])

# Critique prompt
cret_prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        "You are a Twitter tech influencer assistant grading tweets. "
        "Generate a critique and recommendation for the user's tweet. "
        "Always provide detailed feedback including suggestions on length, variety, style, tone, and clarity."
    ),
    MessagesPlaceholder(variable_name='messages')
])

# Initialize LLM
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

# Define chains
generative_chain = gen_prompt | llm
critiqe_chain = cret_prompt | llm
