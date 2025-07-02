import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

