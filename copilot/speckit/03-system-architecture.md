# System Architecture

## Component Map
- **PenTestAgent (agent_backend.py)** ? Orchestrates lifecycle hooks, glues LLM, RAG, memory, and LangChain tools.
- **LLM Layer (ChatOpenAI)** ? Handles prompt/response generation with OPENAI_MODEL.
- **Embedding Layer (OpenAIEmbeddings)** ? Produces vectors for RAG ingestion.
- **Vector Store (ChromaDB)** ? Stores embeddings on disk under CHROMADB_PERSIST_DIR.
- **Persistent Memory (Firestore)** ? Writes engagement documents with interaction arrays.
- **Tool Framework (LangChain Tool + AgentExecutor)** ? Wraps custom functions and exposes them via OpenAI Functions agent.

## Data Flow
1. Startup loads env vars and initializes LLM + embeddings.
2. ChromaDB either loads an existing collection or creates one for pentest_knowledge.
3. Firebase credentials bootstrap Firestore client for engagement memory.
4. Tools registering occurs before creating the OpenAI Functions agent; each tool surfaces descriptive docstrings for schema clarity.
5. handle_command builds an enhanced prompt with [Engagement: name] prefix and passes it to gent_executor.invoke.
6. Agent may call tools as needed; tool outputs are streamed back into the conversation.
7. Final response is returned to caller and recorded in Firestore along with original command and timestamp.

## External Dependencies
- **OpenAI API** ? Requires outbound HTTPS access and API key.
- **Firebase Admin SDK** ? Requires service account JSON; interacts with Firestore.
- **ChromaDB** ? File-system persistence; ensure directory write permissions.

## Extension Points
- self.tools list: append new LangChain Tool objects (custom scan automation, ticketing connectors, etc.).
- Swappable vector store: swap Chroma for managed services if API compatibility maintained.
- Memory backend: Firestore can be replaced by another document DB by implementing _initialize_firestore + _save_interaction equivalents.
- CLI/API interface: main() currently demonstrates CLI usage; future HTTP server can reuse PenTestAgent class directly.

## Risks & Mitigations
- **Missing credentials** ? Provide explicit startup errors and instructions to run .env setup.
- **API rate limits** ? Keep temperature moderate; future backlog includes caching or fallback models.
- **Data sensitivity** ? Encourage sanitization before ingesting customer data into RAG; document retention policies.
