# Data Models

## Firestore Data Models

### Engagement Document
**Collection**: `engagements`  
**Document ID**: `{engagement_name}` (string, e.g., "client-webapp-pentest-2025")

```json
{
  "engagement_name": "string",
  "interactions": [
    {
      "timestamp": "ISO-8601 datetime string",
      "command": "string (user input)",
      "response": "string (agent output)"
    }
  ],
  "last_updated": "ISO-8601 datetime string"
}
```

**Field Descriptions**:
- `engagement_name`: Unique identifier for the penetration testing engagement
- `interactions`: Ordered array of all commands and responses
- `interactions[].timestamp`: When the interaction occurred (ISO-8601 format)
- `interactions[].command`: The user's input command/question
- `interactions[].response`: The agent's generated response
- `last_updated`: Timestamp of most recent update to this document

**Example**:
```json
{
  "engagement_name": "acme-corp-webapp-2025",
  "interactions": [
    {
      "timestamp": "2025-11-29T10:30:00.000Z",
      "command": "Scan 192.168.1.100 for vulnerabilities",
      "response": "Vulnerability Scan Results for 192.168.1.100:\n- Open Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)..."
    },
    {
      "timestamp": "2025-11-29T10:35:00.000Z",
      "command": "What are common XSS prevention techniques?",
      "response": "Based on the knowledge base, common XSS prevention techniques include..."
    }
  ],
  "last_updated": "2025-11-29T10:35:00.000Z"
}
```

---

## Python Data Models

### Agent Response Model
Returned by `PenTestAgent.handle_command()`

```python
{
  "success": bool,
  "response": str,
  "engagement": str,
  "timestamp": str,  # ISO-8601 format
  "error": str | None  # Only present if success=False
}
```

**Field Descriptions**:
- `success`: Whether the command was processed successfully
- `response`: The agent's response text (if successful)
- `engagement`: The engagement name this command was associated with
- `timestamp`: When the command was processed
- `error`: Error message (only present if success=False)

**Success Example**:
```python
{
  "success": True,
  "response": "Based on OWASP guidelines, you should check for SQL injection, XSS, CSRF...",
  "engagement": "demo-engagement-001",
  "timestamp": "2025-11-29T10:30:00.123456"
}
```

**Error Example**:
```python
{
  "success": False,
  "error": "Error processing command: OpenAI API rate limit exceeded",
  "engagement": "demo-engagement-001",
  "timestamp": "2025-11-29T10:30:00.123456"
}
```

---

## ChromaDB Data Models

### Knowledge Document
**Collection**: `pentest_knowledge`

ChromaDB stores documents as:
```python
{
  "id": "auto-generated-uuid",
  "embedding": [0.123, 0.456, ...],  # 1536-dimensional vector (OpenAI embeddings)
  "document": "string (original text)",
  "metadata": {
    # Optional custom metadata
    "source": "OWASP Top 10",
    "category": "web-vulnerabilities",
    "date_added": "2025-11-29"
  }
}
```

**Usage**:
```python
# Adding documents
agent.add_knowledge(
    documents=["SQL Injection is a code injection technique..."],
    metadatas=[{"source": "OWASP", "category": "injection"}]
)

# Searching (internal to knowledge_search tool)
results = vector_store.similarity_search("What is SQL injection?", k=3)
```

---

## LangChain Internal Models

### Conversation Memory (In-Session Only)
```python
{
  "chat_history": [
    HumanMessage(content="What are XSS vulnerabilities?"),
    AIMessage(content="XSS vulnerabilities allow attackers to..."),
    HumanMessage(content="How do I prevent them?"),
    AIMessage(content="To prevent XSS attacks, you should...")
  ]
}
```

**Note**: This is in-memory only and not persisted to Firestore or disk.

---

## Tool Input/Output Models

### knowledge_search Tool
**Input**: 
```python
query: str  # Search query
```

**Output**:
```python
str  # Formatted string with search results
# Example: "Knowledge Base Results:\n\nSQL Injection is...\n\nXSS vulnerabilities..."
```

---

### vulnerability_scan Tool
**Input**:
```python
target: str  # IP address or domain
```

**Output**:
```python
str  # Formatted scan results
# Example:
"""
Vulnerability Scan Results for 192.168.1.100:
- Open Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
- Detected Services: OpenSSH 8.2, Apache 2.4.41
- Potential Vulnerabilities: CVE-2021-3156 (sudo vulnerability)
- Risk Level: Medium
"""
```

---

### get_engagement_context Tool
**Input**:
```python
engagement_name: str
```

**Output**:
```python
str  # JSON-formatted engagement data or error message
# Example: "Engagement Context:\n{\n  'engagement_name': '...', ...}"
```

---

## Configuration Models

### Environment Variables (.env)
```bash
OPENAI_API_KEY="sk-..."  # Required
FIREBASE_CREDENTIALS_PATH="./serviceAccountKey.json"  # Required
OPENAI_MODEL="gpt-4"  # Optional, default: "gpt-4"
CHROMADB_PERSIST_DIR="./chroma_db"  # Optional, default: "./chroma_db"
```

### Firebase Service Account (JSON)
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "firebase-adminsdk-...@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

---

## Type Annotations Reference

```python
from typing import Dict, List, Any, Optional
from datetime import datetime

# Command processing
def handle_command(
    command: str, 
    engagement_name: str
) -> Dict[str, Any]: ...

# Knowledge management
def add_knowledge(
    documents: List[str], 
    metadatas: Optional[List[Dict]] = None
) -> None: ...

# Internal persistence
def _save_interaction(
    engagement_name: str, 
    command: str, 
    response: str
) -> None: ...
```
