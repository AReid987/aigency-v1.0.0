# Product Roadmap

## Phase 1: Core MVP Functionality

**Goal:** Establish the foundational crawling and vector ingestion capabilities.
**Success Criteria:** Users can successfully crawl a URL/sitemap and query the resulting vector index.

### Features

- [ ] Integrate Crawl4AI for basic URL and sitemap crawling - [Implement core crawling logic] `M`
- [ ] Implement simple content extraction (e.g., main article text) - [Extract main content from crawled pages] `S`
- [ ] Integrate LightRAG to create a vector index - [Generate embeddings and store in vector DB] `M`
- [ ] Provide a basic Python API for crawl and query - [Expose core functionality via Python API] `S`

### Dependencies

- Crawl4AI library
- LightRAG library
- Vector database (e.g., ChromaDB)

## Phase 2: Knowledge Graph Integration

**Goal:** Introduce knowledge graph creation and querying capabilities.
**Success Criteria:** Users can extract entities/relationships and perform basic graph queries.

### Features

- [ ] Integrate Graphiti - [Set up Graphiti for graph modeling] `S`
- [ ] Implement basic entity extraction using an LLM - [Use LLM to identify entities from text] `M`
- [ ] Build a simple knowledge graph from extracted entities - [Populate graph DB with entities and relationships] `M`
- [ ] Extend Query API for basic graph queries - [Enable querying the knowledge graph] `S`

### Dependencies

- Graphiti library
- LLM access (e.g., OpenAI, local LLM)
- Graph database (e.g., Neo4j)

## Phase 3: Advanced Configuration and Filtering

**Goal:** Enhance data extraction and update mechanisms.
**Success Criteria:** Users can define custom scraping rules and the knowledge base updates incrementally.

### Features

- [ ] Allow detailed scraping and filtering rules (CSS selectors, etc.) - [Implement flexible content extraction rules] `L`
- [ ] Allow users to define schema for vector and graph data - [Enable custom data modeling] `M`
- [ ] Implement incremental updates for vector DB and KG - [Efficiently update existing knowledge base] `L`

### Dependencies

- Robust parsing libraries
- Schema definition tools

## Phase 4: Scheduling and Monitoring

**Goal:** Provide automation and visibility for the crawling and ingestion process.
**Success Criteria:** Users can schedule recurring crawls and monitor job status.

### Features

- [ ] Add functionality to schedule recurring crawls - [Implement job scheduling] `M`
- [ ] Create a simple dashboard (web UI or CLI) - [Visualize crawl status and metrics] `L`

### Dependencies

- Scheduling library (e.g., APScheduler)
- Basic web framework (if UI)

## Phase 5: Polish and Release

**Goal:** Prepare the product for wider distribution and ensure quality.
**Success Criteria:** Product is well-documented, stable, and easily installable.

### Features

- [ ] Improve documentation and examples - [Comprehensive user guides and code examples] `M`
- [ ] Add comprehensive error handling and logging - [Robust error management and diagnostics] `S`
- [ ] Package the product for distribution (e.g., on PyPI) - [Prepare for public release] `S`

### Dependencies

- Documentation tools (e.g., Sphinx)
- Packaging tools (e.g., setuptools)
