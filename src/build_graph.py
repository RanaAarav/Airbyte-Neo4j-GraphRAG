from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

def transform_graph(tx):
    print("🔄 transforming Raw Airbyte Data into Knowledge Graph...")

    # 1. Extract Users from Raw JSON
    # Airbyte stores data as a string in `_airbyte_data`. We parse it using APOC or Cypher.
    tx.run("""
        MATCH (r:_AirbyteRawGitHubUsers)
        WITH r, apoc.convert.fromJsonMap(r._airbyte_data) AS data
        MERGE (u:User {login: data.login})
        SET u.id = data.id
    """)

    # 2. Extract Issues and Link to Creators
    # This is the "GraphRAG" magic: Connecting disparate data points
    tx.run("""
        MATCH (r:_AirbyteRawGitHubIssues)
        WITH r, apoc.convert.fromJsonMap(r._airbyte_data) AS data
        
        MERGE (i:Issue {id: data.id})
        SET i.title = data.title,
            i.body = data.body
        
        WITH i, data
        MATCH (u:User {login: data.user.login})
        MERGE (u)-[:CREATED]->(i)
    """)
    
    print("Transformation Complete. Graph structure created.")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session() as session:
        session.write_transaction(transform_graph)