# Autonomous Legal Research Assistant

A complete AI-powered legal research system with autonomous agents that retrieve, analyze, and synthesize legal information to generate comprehensive legal briefs with proper citations and jurisdiction analysis.

## Overview

This project implements a modular AI system that answers complex legal queries by:
1. **Retrieving** case law and statutes from legal databases
2. **Analyzing** findings for patterns and legal precedents
3. **Summarizing** key insights and legal principles
4. **Composing** structured legal briefs with citations

## Architecture

### Backend (`/backend`)
- **Python/FastAPI** - REST API with autonomous agent system
- **4 Specialized Agents** - Retriever, Analyzer, Summarizer, Composer
- **Legal Database Integration** - CourtListener, Harvard Caselaw Access
- **Vector Memory** - FAISS/Pinecone for document storage and retrieval
- **Retry Logic & Self-Evaluation** - Robust error handling and quality assurance

### Frontend (`/frontend`)
- **React/TypeScript** - Modern, responsive user interface
- **Real-time Progress** - Live updates during research processing
- **Professional Display** - Structured legal brief presentation
- **Form Handling** - Query validation and submission

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_api_key"
export PINECONE_API_KEY="your_pinecone_api_key"
export COURTLISTENER_API_KEY="your_courtlistener_api_key"

python main.py
```

### Frontend Setup  
```bash
cd frontend
npm install
npm start
```

## Required API Keys

- **OpenAI API** - For GPT-4 language model
- **Pinecone API** - For vector database (optional, falls back to FAISS)
- **CourtListener API** - For legal case database access

## Usage

1. Open `http://localhost:3000` in your browser
2. Navigate to the Research page
3. Enter your legal question (e.g., "Can an employer read employee emails?")
4. Optionally specify jurisdiction
5. Click "Start Research" and wait for AI agents to complete analysis
6. View comprehensive legal brief with citations

## Agent System

### Retriever Agent
- Searches legal databases and vector stores
- Retrieves relevant cases, statutes, and precedents
- Scores findings by relevance and authority

### Analyzer Agent  
- Identifies legal patterns and themes
- Analyzes jurisdictional differences
- Evaluates precedent strength and authority

### Summarizer Agent
- Creates executive summaries
- Extracts key legal findings
- Generates actionable conclusions

### Composer Agent
- Composes structured legal briefs
- Formats citations properly
- Ensures professional legal language

## Features

- **Autonomous AI Agents** with specialized functions  
- **Legal Database Integration** with major legal APIs  
- **Vector Memory System** for document storage  
- **Retry Logic** with exponential backoff  
- **Self-Evaluation** for quality assurance  
- **Structured Legal Briefs** with proper citations  
- **Jurisdiction Analysis** and tagging  
- **Modern React UI** with real-time updates  
- **Professional Grade** legal research output  

## Project Structure

```
├── backend/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── retriever_agent.py
│   │   ├── analyzer_agent.py
│   │   ├── summarizer_agent.py
│   │   └── composer_agent.py
│   ├── config.py
│   ├── models.py
│   ├── vector_store.py
│   ├── legal_apis.py
│   ├── orchestrator.py
│   └── main.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/
    └── public/
```

## Workflow

1. **User Query** → Legal question submitted via frontend
2. **Orchestrator** → Coordinates agent workflow
3. **Retriever** → Searches databases for relevant legal information
4. **Analyzer** → Identifies patterns and legal precedents
5. **Summarizer** → Creates executive summary and key findings
6. **Composer** → Generates final structured legal brief
7. **Response** → Returns comprehensive brief to frontend

## Example Output

The system generates professional legal briefs containing:
- Executive summary answering the legal question
- Key findings with supporting evidence
- Detailed legal analysis with case law
- Practical conclusions and recommendations  
- Supporting case citations with proper formatting
- Jurisdiction-specific analysis and considerations

## Reliability Features

- **Exponential Backoff** for API failures
- **Agent Self-Evaluation** for quality control
- **Graceful Fallbacks** when services are unavailable
- **Comprehensive Error Handling** with detailed logging
- **Input Validation** and query sanitization

## License

This project is licensed under the MIT License. 