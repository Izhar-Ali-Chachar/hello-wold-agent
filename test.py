from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

print(model.invoke('hi').content)