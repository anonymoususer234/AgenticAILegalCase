# Legal Research Assistant Backend

A complete autonomous AI agent system for legal research, built with Python and FastAPI.

## Architecture

This backend implements a multi-agent system for legal research with the following components:

### Core Agents
- **Retriever Agent** (`agents/retriever_agent.py`) - Searches legal databases and vector stores
- **Analyzer Agent** (`agents/analyzer_agent.py`) - Analyzes findings for patterns and precedents  
- **Summarizer Agent** (`agents/summarizer_agent.py`) - Creates executive summaries
- **Composer Agent** (`agents/composer_agent.py`) - Generates structured legal briefs

### Infrastructure
- **Base Agent** (`agents/base_agent.py`) - Common functionality with retry logic and self-evaluation
- **Orchestrator** (`orchestrator.py`) - Coordinates agent workflow and manages research pipeline
- **Vector Store** (`vector_store.py`) - Document storage using FAISS or Pinecone
- **Legal APIs** (`legal_apis.py`) - Integration with CourtListener and Harvard Caselaw Access

### Configuration & Models
- **Config** (`config.py`) - Environment settings and API key management
- **Models** (`models.py`) - Pydantic data models for requests and responses
- **Main** (`main.py`) - FastAPI application with REST endpoints

## Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**
```bash
export OPENAI_API_KEY="your_openai_api_key"
export PINECONE_API_KEY="your_pinecone_api_key" 
export COURTLISTENER_API_KEY="your_courtlistener_api_key"
```

3. **Run the Server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/research` - Submit legal research query
- `GET /api/health` - System health check
- `GET /api/agents/status` - Individual agent status
- `POST /api/validate-query` - Validate research query
- `POST /api/add-documents` - Add documents to vector store
- `GET /api/search` - Search vector store

## Agent Workflow

1. **Retriever** searches legal databases for relevant cases and statutes
2. **Analyzer** identifies patterns, precedents, and jurisdictional differences  
3. **Summarizer** creates executive summaries and key findings
4. **Composer** generates final structured legal brief with citations

Each agent includes:
- Automatic retry with exponential backoff
- Self-evaluation for quality assurance
- Comprehensive error handling

## Configuration

Required API keys:
- OpenAI API (for GPT-4)
- Pinecone API (optional, falls back to FAISS)
- CourtListener API (for legal case access)

## Example Usage

```python
# Submit a legal research query
query = {
    "query": "Can an employer read employee emails?",
    "jurisdiction": "Federal"
}

response = requests.post("http://localhost:8000/api/research", json=query)
legal_brief = response.json()
```

## Legal Database Integration

- **CourtListener**: Federal and state court cases
- **Harvard Caselaw Access**: Historical case law
- **Vector Store**: Local document storage and similarity search

## Retry & Reliability

- Exponential backoff for failed API calls
- Agent self-evaluation for quality control
- Graceful fallback mechanisms
- Comprehensive error reporting

## Features

- Autonomous multi-agent architecture  
- Legal database integration  
- Vector-based document retrieval  
- Structured legal brief generation  
- Citation management and formatting  
- Jurisdiction-specific analysis  
- Real-time API with FastAPI  
- Comprehensive error handling 