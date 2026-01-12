from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

def transform_graph(tx):
    print("Transforming Raw Airbyte Data into Knowledge Graph...")

    tx.run("""
        MATCH (r:_AirbyteRawGitHubUsers)
        WITH r, apoc.convert.fromJsonMap(r._airbyte_data) AS data
        MERGE (u:User {login: data.login})
        SET u.id = data.id
    """)

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
