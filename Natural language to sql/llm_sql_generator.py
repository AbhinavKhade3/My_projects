from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")
)

template = """
You are an expert SQL generator. Based on the user's question and the given database schema, write a syntactically correct SQL query.
NOTE - 
1. Dont give like this ```sql``` ,Just purely give string.
2. Read all Colums and Table name carefully , do not add anything out of them
3. If You are not able to Structure Query return emty string strictly.

Schema:
{schema}

Question:
{question}

SQL Query:
"""

prompt = PromptTemplate(input_variables=["schema", "question"], template=template)
chain = prompt | llm


def generate_sql(schema: str, question: str):
    query = chain.invoke({"schema": schema, "question": question})
    return (query.content).strip()
