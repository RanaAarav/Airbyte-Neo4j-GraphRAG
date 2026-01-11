import json
import random
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

def seed_data(tx):
    print("Seeding Mock Airbyte Tables...")
    
    # 1. Mock GitHub Users (Raw JSON format like Airbyte)
    users = [
        {"login": "dev_guru", "id": 101},
        {"login": "ai_wizard", "id": 102},
        {"login": "bug_hunter", "id": 103}
    ]
    
    for u in users:
        tx.run("""
            CREATE (n:_AirbyteRawGitHubUsers {
                _airbyte_data: $data, 
                _airbyte_ab_id: randomUUID()
            })
        """, data=json.dumps(u))

    # 2. Mock GitHub Issues
    issues = [
        {"id": 1, "title": "Login fails on Safari", "user": {"login": "bug_hunter"}, "body": "Auth error 500"},
        {"id": 2, "title": "Add Graph support", "user": {"login": "dev_guru"}, "body": "We need Neo4j"},
        {"id": 3, "title": "Fix Memory Leak", "user": {"login": "ai_wizard"}, "body": "OOM Exception"}
    ]

    for i in issues:
        tx.run("""
            CREATE (n:_AirbyteRawGitHubIssues {
                _airbyte_data: $data,
                _airbyte_ab_id: randomUUID()
            })
        """, data=json.dumps(i))
        
    print("Seeding Complete. Neo4j now mimics an Airbyte destination.")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session() as session:
        session.write_transaction(seed_data)