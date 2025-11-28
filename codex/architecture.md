# Architecture

## System Overview
The PenTest AI Agent follows a modular architecture with four main layers:

```
┌─────────────────────────────────────────┐
│         Frontend / API Layer            │
│    (Future: React Canvas Interface)     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Agent Orchestration Layer        │
│     - Command Processing                │
│     - LangChain Agent Executor          │
│     - Conversation Memory               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          Core Components                │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌────────────────┐   │
│  │ LLM Layer   │  │  RAG System    │   │
│  │ (GPT-4)     │  │  (ChromaDB)    │   │
│  └─────────────┘  └────────────────┘   │
│                                         │
│  ┌─────────────┐  ┌────────────────┐   │
│  │ Tool        │  │  Persistent    │   │
│  │ Framework   │  │  Memory        │   │
│  │             │  │  (Firestore)   │   │
│  └─────────────┘  └────────────────┘   │
└─────────────────────────────────────────┘
```

## Component Details

### 1. LLM Integration Layer
- **Responsibility**: Natural language processing and generation
- **Technology**: OpenAI GPT-4 via LangChain
- **Key Features**:
  - Conversational understanding
  - Tool selection and execution planning
  - Response generation

### 2. RAG System
- **Responsibility**: Knowledge retrieval and semantic search
- **Technology**: ChromaDB with OpenAI embeddings
- **Key Features**:
  - Vector similarity search
  - Document storage and retrieval
  - Persistent storage on disk
  - Configurable collection management

### 3. Persistent Memory
- **Responsibility**: Long-term engagement tracking
- **Technology**: Firebase/Firestore
- **Key Features**:
  - Engagement history storage
  - Interaction logging
  - Cross-session persistence
  - Document-based data model

### 4. Tool Execution Framework
- **Responsibility**: Execute security operations and utilities
- **Technology**: LangChain Tools interface
- **Built-in Tools**:
  - `knowledge_search`: Query the RAG knowledge base
  - `vulnerability_scan`: Simulated vulnerability scanning
  - `get_engagement_context`: Retrieve engagement history
- **Extensibility**: Easy to add custom tools via Tool interface

### 5. Agent Orchestration
- **Responsibility**: Coordinate components and manage workflow
- **Technology**: LangChain AgentExecutor
- **Key Features**:
  - Command routing
  - Tool invocation
  - Conversation memory (in-session)
  - Error handling

## Data Flow

### Command Processing Flow
```
User Command → Agent Executor → LLM (tool selection) 
                                      ↓
                          ┌───────────┴────────────┐
                          ↓                        ↓
                    RAG Retrieval            Tool Execution
                          ↓                        ↓
                    LLM (synthesis) ← ─────────────┘
                          ↓
                    Response + Firestore Save
                          ↓
                    Return to User
```

### Knowledge Addition Flow
```
Documents → OpenAI Embeddings → ChromaDB Storage → Disk Persistence
```

### Engagement Tracking Flow
```
Command/Response → Firestore Document Update → Cloud Persistence
```

## Storage Schema

### ChromaDB
- **Collection**: `pentest_knowledge`
- **Storage**: Local disk at `./chroma_db/`
- **Content**: Embedded security knowledge documents

### Firestore
- **Collection**: `engagements`
- **Document ID**: `{engagement_name}`
- **Schema**: See data-models.md

## Configuration Management
- Environment variables via `.env` file
- Secrets never committed to version control
- Service account credentials stored separately
- Configurable model selection and storage paths
