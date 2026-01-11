GraphRAG Pipeline: Ingesting Siloed Data into Knowledge Graphs
==============================================================

![Airbyte](https://img.shields.io/badge/ETL-Airbyte-blue)
![Neo4j](https://img.shields.io/badge/DB-Neo4j-green)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange)

**The Problem:** Standard Vector RAG is relationship-blind. It treats data as a flat list of embeddings, failing to connect the dots between related entities (e.g., a Bug Report connected to a specific User and a Code Release).

**The Solution:** An automated pipeline that turns raw data into a Knowledge Graph. We use Airbyte to ingest structured data from SaaS sources and Neo4j to store the semantic relationships.

Architecture
------------

1.  **Ingestion:** Airbyte extracts data from sources (GitHub/Jira/Postgres).
2.  **Storage:** Neo4j captures the data as nodes.
3.  **Semantic Linkage:** A Python-based transformation layer (built with Python 3.14) parses raw JSON and creates graph edges (`:CREATED`, `:DEPENDS_ON`).
4.  **Reasoning:** Gemini 3.0 Pro translates natural language into Cypher queries.
    
Features
--------

*   **Agentic Retrieval:** Uses Gemini 3.0 to traverse complex graph paths.
*   **Modular ETL:** Airbyte manages the API data extraction.
*   **Schema-Aware:** Strict prompts ensure high-accuracy Cypher generation.

Setup
-----
1.  Start Neo4j: ```bash docker-compose up -d```
2.  Seed Mock Data: ```bash python src/seed_airbyte_data.py```
3.  Build Graph: ```bash python src/build_graph.py```
4.  Query AI: ```bash python src/query_graph.py```
