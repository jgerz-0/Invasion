# Functional & Non-Functional Requirements

## Core Functional Requirements
1. **Command Processing** ? Accept text commands, wrap them with engagement metadata, and invoke the LangChain agent executor.
2. **LLM Responses** ? Use GPT-4 via ChatOpenAI with temperature controls to produce contextual responses.
3. **Knowledge Retrieval (RAG)** ? Ingest plaintext documents, embed them with OpenAI embeddings, and store in ChromaDB. Serve similarity search results (top 3 docs) to ground LLM outputs.
4. **Persistent Engagement Memory** ? Store every command/response pair inside Firestore under engagements/{name} with ISO-8601 timestamps.
5. **Tool Invocation** ? Provide built-in tools for knowledge search, simulated vulnerability scans, and engagement context retrieval. Additional tools must follow LangChain Tool conventions.
6. **Error Handling** ? Fail gracefully when dependencies (OpenAI, Firestore, Chroma) are unavailable, returning structured error payloads.

## Tool Catalog Expectations
| Tool | Purpose | Inputs | Outputs |
| --- | --- | --- | --- |
| knowledge_search | Retrieve relevant pentest knowledge snippets | Natural language query | Joined paragraph string (top matching docs) |
| ulnerability_scan | Return canned findings to mimic scanner data | Target identifier, scan scope description | JSON-like text summarizing vulnerabilities |
| get_engagement_context | Pull historical interactions from Firestore | Engagement name | Structured summary (command, response, timestamp list) |
| Custom tools | Extensible wrappers for scripts/APIs | Defined per tool | Freeform but documented |

## Configuration & Security Requirements
- .env driven configuration for API keys, Firestore cert path, model name, and Chroma persistence dir.
- Reject startup if OPENAI_API_KEY is missing; warn (not crash) when Chroma/Firestore are unavailable.
- Keep credentials out of version control (.env, serviceAccountKey.json).
- Provide logging that avoids leaking secrets while still surfacing initialization failures.

## Non-Functional Requirements
- **Performance**: Respond to single prompts in <5 seconds assuming upstream APIs respond normally.
- **Reliability**: Record ?95% of interactions when Firestore is configured, with retry/backoff hooks ready for future implementation.
- **Extensibility**: Adding a new tool or storage backend should not require changes to core PenTestAgent.handle_command logic.
- **Deployability**: Can run from CLI (python agent_backend.py) with virtualenv-managed dependencies.
- **Observability**: Console output should trace initialization events (LLM, RAG, Firestore) for troubleshooting.
