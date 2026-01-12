GraphRAG Pipeline: Airbyte Ingestion to Neo4j Knowledge Graph
=============================================================

![Airbyte](https://img.shields.io/badge/ETL-Airbyte-blue)
![Neo4j](https://img.shields.io/badge/DB-Neo4j-green)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange)

This project implements an automated pipeline for building Knowledge Graphs to support GraphRAG applications. It solves the relational blindness inherent in standard vector-based RAG by preserving semantic links between ingested entities.

Architecture
------------
1.  Ingestion: Utilizes Airbyte to extract structured data from SaaS sources into Neo4j.
2.  Transformation: A Python-based logic layer parses raw JSON blobs into a schema-defined graph.
3.  Semantic Linkage: A Python-based transformation layer (built with Python 3.14) parses raw JSON and creates graph edges (`:CREATED`, `:DEPENDS_ON`).
4.  Retrieval: Uses Gemini 3.0 Pro to translate natural language queries into Cypher statements.

Requirements
------------
*    Docker and Docker Compose
*    Python 3.11+
*    Google Gemini API Key

Execution Flow
--------------
1.  Start Neo4j: ```docker-compose up -d```
2.  Seed Mock Data: ```python src/seed_airbyte_data.py``` (Simulates Airbyte Raw destination)
3.  Build Graph: ```python src/build_graph.py```
4.  Run Agent: ```python src/query_graph.py```
