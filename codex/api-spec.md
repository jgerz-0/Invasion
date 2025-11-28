# API Specification

## Overview
The PenTest AI Agent Backend provides a **Python class-based interface** (not REST API). It is designed to be imported and used programmatically.

**Note**: This is not a web API. For web integration, wrap these methods in a Flask/FastAPI application.

---

## Class: PenTestAgent

### Constructor

#### `__init__()`
Initializes the PenTest Agent with all required components.

**Parameters**: None (reads from environment variables)

**Environment Variables Required**:
- `OPENAI_API_KEY` (required)
- `FIREBASE_CREDENTIALS_PATH` (required)
- `OPENAI_MODEL` (optional, default: "gpt-4")
- `CHROMADB_PERSIST_DIR` (optional, default: "./chroma_db")

**Returns**: `PenTestAgent` instance

**Raises**:
- `ValueError` if `OPENAI_API_KEY` not found

**Side Effects**:
- Initializes OpenAI LLM and embeddings
- Creates/loads ChromaDB vector store
- Initializes Firebase/Firestore connection
- Sets up LangChain agent and tools

**Example**:
```python
from agent_backend import PenTestAgent

agent = PenTestAgent()
```

---

## Public Methods

### `handle_command(command: str, engagement_name: str) -> Dict[str, Any]`
Main entry point for processing user commands.

**Parameters**:
- `command` (str): The user's natural language command or question
- `engagement_name` (str): Identifier for the current penetration testing engagement

**Returns**: Dictionary with structure:
```python
{
    "success": bool,
    "response": str,  # AI-generated response (if success=True)
    "engagement": str,  # Same as engagement_name parameter
    "timestamp": str,  # ISO-8601 format
    "error": str  # Only present if success=False
}
```

**Side Effects**:
- Saves interaction to Firestore
- Updates agent's conversation memory (in-session)
- May invoke tools (RAG search, vulnerability scan, etc.)

**Example**:
```python
response = agent.handle_command(
    command="What are the OWASP Top 10 vulnerabilities?",
    engagement_name="acme-webapp-2025"
)

if response["success"]:
    print(response["response"])
else:
    print(f"Error: {response['error']}")
```

**Error Handling**:
- Catches all exceptions and returns `success=False` with error message
- Continues operation even if Firestore is unavailable (logs warning)

---

### `add_knowledge(documents: List[str], metadatas: Optional[List[Dict]] = None) -> None`
Add documents to the RAG knowledge base.

**Parameters**:
- `documents` (List[str]): List of text documents to add to ChromaDB
- `metadatas` (Optional[List[Dict]]): Optional metadata for each document
  - Must be same length as `documents` if provided
  - Example: `[{"source": "OWASP", "category": "web"}]`

**Returns**: None

**Side Effects**:
- Generates embeddings via OpenAI API
- Stores vectors in ChromaDB
- Persists to disk

**Example**:
```python
knowledge_docs = [
    "SQL Injection is a code injection technique that exploits vulnerabilities in database queries.",
    "Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages.",
]

metadata = [
    {"source": "OWASP", "category": "injection"},
    {"source": "OWASP", "category": "xss"}
]

agent.add_knowledge(knowledge_docs, metadata)
```

**Error Handling**:
- Prints error message if vector store not initialized
- Catches and prints exceptions during embedding/storage

---

## Private Methods (Internal Use)

### `_initialize_llm() -> None`
Initializes OpenAI LLM and embeddings.

**Internal Use Only**: Called by `__init__()`

---

### `_initialize_rag() -> None`
Initializes ChromaDB vector store for RAG.

**Internal Use Only**: Called by `__init__()`

---

### `_initialize_firestore() -> None`
Initializes Firebase/Firestore client.

**Internal Use Only**: Called by `__init__()`

---

### `_initialize_tools() -> None`
Initializes available tools for the agent.

**Internal Use Only**: Called by `__init__()`

**Tools Created**:
- `knowledge_search`: Search RAG knowledge base
- `vulnerability_scan`: Simulated vulnerability scanning
- `get_engagement_context`: Retrieve engagement history

---

### `_initialize_agent() -> None`
Initializes LangChain agent executor.

**Internal Use Only**: Called by `__init__()`

---

### `_save_interaction(engagement_name: str, command: str, response: str) -> None`
Saves interaction to Firestore.

**Internal Use Only**: Called by `handle_command()`

**Parameters**:
- `engagement_name` (str): Engagement identifier
- `command` (str): User's command
- `response` (str): Agent's response

**Firestore Operations**:
- Reads existing document or creates new one
- Appends interaction to `interactions` array
- Updates `last_updated` timestamp

---

## Tools (Available to Agent)

The agent has access to the following tools via LangChain:

### Tool: `knowledge_search`
**Description**: "Search the penetration testing knowledge base for techniques, vulnerabilities, and best practices."

**Input**: 
```python
query: str  # Search query
```

**Output**: 
```python
str  # Top 3 most relevant documents or "No relevant information found"
```

**Example (internal to agent)**:
```
knowledge_search("SQL injection prevention")
→ "Knowledge Base Results:\n\nSQL Injection can be prevented by using parameterized queries..."
```

---

### Tool: `vulnerability_scan`
**Description**: "Perform a simulated vulnerability scan on a target IP or domain."

**Input**:
```python
target: str  # IP address or domain name
```

**Output**:
```python
str  # Formatted scan results (currently simulated)
```

**Example (internal to agent)**:
```
vulnerability_scan("192.168.1.100")
→ "Vulnerability Scan Results for 192.168.1.100:\n- Open Ports: 22, 80, 443\n..."
```

---

### Tool: `get_engagement_context`
**Description**: "Retrieve historical context and data for a specific penetration testing engagement."

**Input**:
```python
engagement_name: str  # Engagement identifier
```

**Output**:
```python
str  # JSON-formatted engagement data or error message
```

**Example (internal to agent)**:
```
get_engagement_context("acme-webapp-2025")
→ "Engagement Context:\n{\n  'engagement_name': 'acme-webapp-2025',\n  'interactions': [...]\n}"
```

---

## Usage Patterns

### Basic Usage
```python
from agent_backend import PenTestAgent

# Initialize
agent = PenTestAgent()

# Process commands
result = agent.handle_command(
    "Scan 10.0.0.1 for vulnerabilities",
    "engagement-001"
)
print(result["response"])
```

### With Knowledge Base
```python
# Add security knowledge
agent.add_knowledge([
    "OWASP Top 10 includes: SQL Injection, XSS, Broken Authentication...",
    "Port scanning with Nmap: nmap -sV -sC target.com"
])

# Query knowledge
result = agent.handle_command(
    "How do I scan for open ports?",
    "engagement-001"
)
```

### Error Handling
```python
result = agent.handle_command(command, engagement)

if not result["success"]:
    logger.error(f"Agent error: {result['error']}")
    # Implement retry logic or fallback
else:
    process_response(result["response"])
```

---

## Future API Endpoints (Not Implemented)

If wrapped in a web framework (FastAPI example):

```python
# Example FastAPI wrapper (not included)
from fastapi import FastAPI
from agent_backend import PenTestAgent

app = FastAPI()
agent = PenTestAgent()

@app.post("/api/command")
def execute_command(command: str, engagement: str):
    return agent.handle_command(command, engagement)

@app.post("/api/knowledge")
def add_knowledge(documents: List[str]):
    agent.add_knowledge(documents)
    return {"status": "success"}
```

**Note**: Security, authentication, and rate limiting would be required for production use.
