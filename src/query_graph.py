import os
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. Connect to Neo4j
graph = Neo4jGraph(
    url="bolt://localhost:7687", 
    username="neo4j", 
    password="password"
)

graph.refresh_schema()

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
    convert_system_message_to_human=True
)

# 3. Define a Strict Prompt (The Fix)
# We tell the AI exactly what the Nodes and Relationships look like.
CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}

CRITICAL RULES:
1. For User nodes, ALWAYS use the property 'login'. Do NOT use 'name' or 'username'.
2. For Issue nodes, use 'title' and 'body'.
3. The relationship is [:CREATED], not [:CREATED_BY].
4. When searching for titles, ALWAYS use 'CONTAINS' (case-insensitive) instead of exact match.

The question is:
{question}
"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], 
    template=CYPHER_GENERATION_TEMPLATE
)

# 4. Create the Chain with the Prompt
chain = GraphCypherQAChain.from_llm(
    llm, 
    graph=graph, 
    verbose=True,
    cypher_prompt=CYPHER_PROMPT, # Inject the rules
    allow_dangerous_requests=True
)

def ask(question):
    print(f"\nUser: {question}")
    try:
        res = chain.invoke(question)
        print(f"AI: {res['result']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ask("Who created the issue about 'Memory Leak'?")
    ask("How many issues did 'dev_guru' create?")