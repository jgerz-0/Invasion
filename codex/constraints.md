# Constraints

## Technical Constraints

### API Dependencies
- **OpenAI API Required**: Must have valid API key with GPT-4 access
- **Rate Limits**: Subject to OpenAI API rate limits based on account tier
- **Firebase Required**: Must have Firebase project with Firestore enabled
- **Firestore Quotas**: Subject to Firebase free tier or paid plan limits

### Python Environment
- **Python Version**: Requires Python 3.8 or higher
- **Virtual Environment**: Strongly recommended for dependency isolation
- **Package Dependencies**: Must install all packages from requirements.txt

### Storage Requirements
- **Disk Space**: ChromaDB persistence directory must have write access
- **Firestore Access**: Service account must have read/write permissions
- **Local Storage**: ChromaDB stores vectors on local disk (can grow large)

### Performance
- **Response Time**: Typical 2-10 seconds per command (depends on LLM + tools)
- **Synchronous Execution**: Tools execute synchronously (blocking)
- **Single-Threaded**: Not designed for concurrent request handling
- **Memory Usage**: LangChain and ChromaDB require sufficient RAM

---

## Business Constraints

### Security & Compliance
- **API Key Security**: All secrets must be in .env file (never committed)
- **Service Account**: Firebase JSON credentials must be secured
- **Data Privacy**: Engagement data stored in cloud (Firestore)
- **Audit Trail**: All interactions logged (consider data retention policies)

### Licensing
- **OpenAI Terms**: Subject to OpenAI usage policies
- **Firebase Terms**: Subject to Google Cloud/Firebase terms
- **Open Source**: Dependencies use various open source licenses

### Cost
- **OpenAI API**: Pay-per-token usage (can be expensive with GPT-4)
- **Firebase**: Free tier available, costs scale with usage
- **Embeddings**: Additional cost for OpenAI embeddings API

---

## Functional Constraints

### LLM Limitations
- **Model Hallucination**: LLM may generate incorrect information
- **Context Window**: Limited by GPT-4 context size (8K or 32K)
- **Tool Reliability**: Depends on LLM correctly selecting tools
- **No Guarantees**: AI responses are probabilistic, not deterministic

### RAG Limitations
- **Knowledge Quality**: Only as good as documents added to ChromaDB
- **Retrieval Accuracy**: May not find relevant docs if embeddings don't match
- **Cold Start**: Empty knowledge base provides no value
- **Manual Curation**: Requires someone to add quality documents

### Persistence Limitations
- **Session Memory**: ConversationBufferMemory not persisted between runs
- **Firestore Only**: Engagement history only in Firestore (no local backup)
- **Network Dependent**: Requires internet for Firestore and OpenAI

### Tool Constraints
- **Mock Scanning**: vulnerability_scan is simulated (not real)
- **No Real Tools**: Requires integration work for actual security tools
- **Synchronous Only**: Long-running tools block the entire response

---

## Design Constraints

### Architecture
- **Single Agent**: Not designed for multi-agent orchestration
- **Monolithic**: All logic in single agent_backend.py file
- **No API**: Python class interface only (no REST endpoints)
- **No Frontend**: Backend only (requires separate UI)

### Extensibility
- **Tool Interface**: New tools must implement LangChain Tool interface
- **No Plugin System**: No formal plugin architecture
- **Manual Integration**: Adding tools requires code changes

### Scalability
- **Single Instance**: Not designed for horizontal scaling
- **No Load Balancing**: One agent per process
- **No Queue**: No async job queue for background tasks
- **Session State**: In-memory state doesn't scale across instances

---

## Development Constraints

### Environment Setup
- **Manual Configuration**: .env file must be manually created
- **Firebase Setup**: Requires Firebase console access to create project
- **Service Account**: Must manually download and secure JSON key

### Testing
- **No Unit Tests**: Test suite not included in spec kit
- **Mock Dependencies**: Testing requires mocking OpenAI and Firebase
- **Integration Testing**: Difficult without real API keys

### Deployment
- **Not Production Ready**: Requires security hardening for production
- **No Containerization**: Dockerfile not included (recommended for deployment)
- **No CI/CD**: Build/deploy pipeline not included
- **Manual Dependency Install**: pip install required for setup

---

## Non-Negotiable Constraints

### Security
- ❌ **NEVER commit .env or serviceAccountKey.json**
- ❌ **NEVER hardcode API keys in code**
- ❌ **NEVER expose API keys in logs or errors**

### Data Handling
- ❌ **NEVER store sensitive customer data without encryption**
- ❌ **NEVER share API keys between environments**

### Code Quality
- ✅ **MUST handle API errors gracefully**
- ✅ **MUST validate inputs before processing**
- ✅ **MUST log errors for debugging**
