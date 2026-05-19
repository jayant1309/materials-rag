# Graph Report - .  (2026-05-19)

## Corpus Check
- Corpus is ~1,967 words - fits in a single context window. You may not need a graph.

## Summary
- 78 nodes · 87 edges · 18 communities (14 shown, 4 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_PDF Parsing|PDF Parsing]]
- [[_COMMUNITY_Core Engine Orchestration|Core Engine Orchestration]]
- [[_COMMUNITY_Application Configuration|Application Configuration]]
- [[_COMMUNITY_Query Processing|Query Processing]]
- [[_COMMUNITY_Ingestion Pipeline|Ingestion Pipeline]]
- [[_COMMUNITY_Ragas Evaluation|Ragas Evaluation]]
- [[_COMMUNITY_Gemini Settings Hooks|Gemini Settings Hooks]]
- [[_COMMUNITY_Logging Utilities|Logging Utilities]]
- [[_COMMUNITY_PDF Parser Rationale|PDF Parser Rationale]]
- [[_COMMUNITY_README Documentation|README Documentation]]

## God Nodes (most connected - your core abstractions)
1. `IndexManager` - 13 edges
2. `IngestionManager` - 7 edges
3. `MaterialsRAGQueryEngine` - 7 edges
4. `load_config()` - 6 edges
5. `MarkerParser` - 6 edges
6. `NougatParser` - 6 edges
7. `BasePDFParser` - 5 edges
8. `get_parser()` - 5 edges
9. `RagasEvaluator` - 5 edges
10. `SourceNode` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Modular Design Principle` --rationale_for--> `IngestionManager`  [EXTRACTED]
  GEMINI.md → src/ingestion/pipeline.py
- `Application Settings` --conceptually_related_to--> `YAML Configuration`  [EXTRACTED]
  src/config.py → configs/config.yaml
- `SourceNode` --uses--> `IndexManager`  [INFERRED]
  src/engine/query_engine.py → src/engine/index_manager.py
- `QueryResult` --uses--> `IndexManager`  [INFERRED]
  src/engine/query_engine.py → src/engine/index_manager.py
- `IngestionManager` --calls--> `IndexManager`  [EXTRACTED]
  src/ingestion/pipeline.py → src/engine/index_manager.py

## Hyperedges (group relationships)
- **RAG Orchestration Flow** — ui_app_app, engine_query_engine_materialsragqueryengine, engine_index_manager_indexmanager [INFERRED 0.95]
- **Data Ingestion Path** — ui_app_app, ingestion_pipeline_ingestionmanager, ingestion_pdf_parser_markerparser, engine_index_manager_indexmanager [INFERRED 0.95]

## Communities (18 total, 4 thin omitted)

### Community 0 - "PDF Parsing"
Cohesion: 0.19
Nodes (11): ABC, BasePDFParser, get_parser(), MarkerParser, NougatParser, Abstract base class for PDF parsers., PDF parser using the Marker library for high-quality markdown extraction., Parses a PDF using Marker.                  Note: This assumes Marker is install (+3 more)

### Community 1 - "Core Engine Orchestration"
Cohesion: 0.18
Nodes (9): YAML Configuration, IndexManager, Manages the creation and loading of the VectorStoreIndex with ChromaDB., Initializes or loads the VectorStoreIndex from ChromaDB.                  Return, Adds documents to the index and persists them., MaterialsRAGQueryEngine, Core Query Engine for the Materials Science Research Assistant., Application Settings (+1 more)

### Community 2 - "Application Configuration"
Cohesion: 0.27
Nodes (11): BaseSettings, AppSettings, EmbeddingSettings, LLMSettings, load_config(), Settings for the Large Language Model (Ollama)., Settings for the embedding model., Settings for vector storage and data paths. (+3 more)

### Community 3 - "Query Processing"
Cohesion: 0.32
Nodes (6): BaseModel, QueryResult, Represents a source node for a query response., Structured result of a RAG query., Executes a query against the RAG system.                  Args:             quer, SourceNode

### Community 4 - "Ingestion Pipeline"
Cohesion: 0.29
Nodes (4): Modular Design Principle, IngestionManager, Manages the ingestion pipeline from PDF to Vector Store., Parses all PDFs in a directory and runs them through the ingestion pipeline.

### Community 5 - "Ragas Evaluation"
Cohesion: 0.33
Nodes (3): RagasEvaluator, Evaluates the RAG system performance using Ragas metrics., Runs Ragas evaluation on a set of test questions.                  Args:

## Knowledge Gaps
- **3 isolated node(s):** `BeforeTool`, `Materials Science RAG Project`, `YAML Configuration`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IndexManager` connect `Core Engine Orchestration` to `Query Processing`, `Ingestion Pipeline`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **Why does `IngestionManager` connect `Ingestion Pipeline` to `Core Engine Orchestration`?**
  _High betweenness centrality (0.213) - this node is a cross-community bridge._
- **Why does `get_parser()` connect `PDF Parsing` to `Ingestion Pipeline`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `IndexManager` (e.g. with `SourceNode` and `QueryResult`) actually correct?**
  _`IndexManager` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `BeforeTool`, `Settings for the Large Language Model (Ollama).`, `Settings for the embedding model.` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._