# Airbyte to Neo4j GraphRAG Pipeline

![Airbyte](https://img.shields.io/badge/ETL-Airbyte-blue)
![Neo4j](https://img.shields.io/badge/DB-Neo4j-green)
![LangChain](https://img.shields.io/badge/AI-LangChain-orange)

A complete **Knowledge Graph** pipeline. This project demonstrates how to turn raw unstructured data (ingested via **Airbyte**) into a semantic graph for **GraphRAG** applications.

## 🏗 Architecture

1.  **Ingest:** Airbyte pulls data (e.g., GitHub/Jira) into Neo4j as raw JSON nodes.
2.  **Transform:** Python scripts parse the raw JSON and construct relationships (`:CREATED`, `:BLOCKED_BY`).
3.  **Query:** A LangChain Agent translates natural language into **Cypher** queries.

## 🚀 Quick Start

### 1. Start Database
```bash
docker-compose up -d