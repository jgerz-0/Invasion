# Development Guide

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- OpenAI API account with GPT-4 access
- Google Firebase account

### Initial Setup

#### 1. Clone or Navigate to Project
```powershell
cd c:\Users\User\Invasion
```

#### 2. Create Virtual Environment
```powershell
# Create venv
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\activate

# Verify activation (should show venv in path)
python --version
```

#### 3. Install Dependencies
```powershell
# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- openai
- langchain
- langchain-openai
- langchain-community
- chromadb
- python-dotenv
- firebase-admin
- pydantic
- requests

#### 4. Configure Environment Variables
```powershell
# Copy example to create .env
Copy-Item .env.example .env

# Edit .env with your credentials
notepad .env
```

Add your actual values:
```env
OPENAI_API_KEY="sk-your-actual-key-here"
FIREBASE_CREDENTIALS_PATH="./serviceAccountKey.json"
OPENAI_MODEL="gpt-4"
CHROMADB_PERSIST_DIR="./chroma_db"
```

#### 5. Setup Firebase
1. Go to https://console.firebase.google.com/
2. Create new project or select existing
3. Enable Cloud Firestore:
   - Navigate to **Firestore Database**
   - Click **Create Database**
   - Choose **Start in test mode** (for development)
4. Generate service account key:
   - Go to **Project Settings** → **Service Accounts**
   - Click **Generate New Private Key**
   - Save as `serviceAccountKey.json` in project root
5. **IMPORTANT**: Add to `.gitignore` (already done)

#### 6. Test the Setup
```powershell
# Run the agent
python agent_backend.py
```

Expected output:
```
============================================================
PenTest AI Agent - Backend Initialization
============================================================
✓ LLM initialized: gpt-4
✓ RAG system initialized with ChromaDB at ./chroma_db
✓ Firestore initialized for persistent memory
✓ Initialized 3 tools
✓ Agent executor initialized

============================================================
Agent Ready!
============================================================
```

---

## Project Structure

```
Invasion/
├── codex/                      # Codex spec kit files
│   ├── project-brief.md
│   ├── tech-stack.md
│   ├── architecture.md
│   ├── features.md
│   ├── constraints.md
│   ├── data-models.md
│   ├── api-spec.md
│   └── development-guide.md
├── venv/                       # Virtual environment (git-ignored)
├── chroma_db/                  # ChromaDB persistence (git-ignored)
├── agent_backend.py            # Main agent implementation
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (git-ignored)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── serviceAccountKey.json     # Firebase credentials (git-ignored)
└── README.md                  # Project documentation
```

---

## Development Workflow

### Making Changes

#### 1. Activate Virtual Environment
Always activate before working:
```powershell
.\venv\Scripts\activate
```

#### 2. Make Code Changes
Edit `agent_backend.py` or add new files.

#### 3. Test Changes
```powershell
python agent_backend.py
```

#### 4. Install New Dependencies
If adding new packages:
```powershell
pip install <package-name>
pip freeze > requirements.txt
```

### Adding New Tools

To extend the agent with custom tools:

```python
# In agent_backend.py, inside _initialize_tools()

def my_custom_tool(input_param: str) -> str:
    """Description of what this tool does."""
    # Your implementation
    return f"Result: {input_param}"

self.tools.append(Tool(
    name="my_custom_tool",
    func=my_custom_tool,
    description="Clear description for the LLM to understand when to use this tool"
))
```

### Adding Knowledge to RAG

```python
# Add security knowledge documents
security_docs = [
    "OWASP Top 10 2021: A01:2021 – Broken Access Control...",
    "Nmap scanning: Use -sV for version detection...",
    "SQL Injection: Always use parameterized queries..."
]

agent.add_knowledge(security_docs, metadatas=[
    {"source": "OWASP", "year": "2021"},
    {"source": "Nmap Docs", "category": "scanning"},
    {"source": "OWASP", "category": "injection"}
])
```

---

## Testing

### Manual Testing

```python
from agent_backend import PenTestAgent

agent = PenTestAgent()

# Test command processing
response = agent.handle_command(
    "What is SQL injection?",
    "test-engagement"
)
print(response)

# Test knowledge search
agent.add_knowledge(["SQL injection is a code injection attack..."])
response = agent.handle_command(
    "How does SQL injection work?",
    "test-engagement"
)
print(response)

# Test engagement persistence
response = agent.handle_command(
    "Show me the history for test-engagement",
    "test-engagement"
)
print(response)
```

### Unit Testing (Future)

Create `tests/test_agent.py`:
```python
import pytest
from unittest.mock import Mock, patch
from agent_backend import PenTestAgent

@patch('agent_backend.ChatOpenAI')
@patch('agent_backend.firebase_admin.initialize_app')
def test_agent_initialization(mock_firebase, mock_llm):
    agent = PenTestAgent()
    assert agent is not None
    assert agent.llm is not None
```

---

## Common Development Tasks

### Update Dependencies
```powershell
pip install --upgrade -r requirements.txt
```

### Clear ChromaDB (Reset Knowledge Base)
```powershell
Remove-Item -Recurse -Force .\chroma_db\
# Restart agent to recreate
```

### View Firestore Data
1. Go to Firebase Console
2. Navigate to **Firestore Database**
3. Browse `engagements` collection

### Debug Mode
Add to `agent_backend.py`:
```python
self.agent_executor = AgentExecutor(
    agent=agent,
    tools=self.tools,
    memory=self.memory,
    verbose=True,  # Shows LLM reasoning
    handle_parsing_errors=True
)
```

---

## Troubleshooting

### Issue: Import Errors
**Error**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### Issue: OpenAI API Error
**Error**: `AuthenticationError: Incorrect API key provided`

**Solution**:
1. Check `.env` has correct `OPENAI_API_KEY`
2. Verify key at https://platform.openai.com/api-keys
3. Ensure no extra spaces or quotes

---

### Issue: Firebase Connection Failed
**Error**: `Could not initialize Firestore`

**Solution**:
1. Verify `serviceAccountKey.json` exists
2. Check path in `.env` is correct
3. Ensure Firestore is enabled in Firebase Console
4. Verify service account has permissions

---

### Issue: ChromaDB Persistence Error
**Error**: `Permission denied: './chroma_db'`

**Solution**:
```powershell
# Ensure directory is writable
New-Item -ItemType Directory -Force -Path .\chroma_db
```

---

### Issue: Rate Limit Exceeded
**Error**: `RateLimitError: You exceeded your current quota`

**Solution**:
1. Check OpenAI account billing
2. Reduce request frequency
3. Consider upgrading OpenAI plan
4. Implement exponential backoff

---

## Best Practices

### Security
- ✅ Never commit `.env` or `serviceAccountKey.json`
- ✅ Rotate API keys regularly
- ✅ Use separate Firebase projects for dev/prod
- ✅ Enable Firestore security rules in production

### Code Quality
- ✅ Add type hints to all functions
- ✅ Document complex logic with comments
- ✅ Handle errors gracefully (try/except)
- ✅ Log important events

### Performance
- ✅ Limit ChromaDB search results (k parameter)
- ✅ Use smaller models for testing (gpt-3.5-turbo)
- ✅ Cache frequently used knowledge
- ✅ Implement rate limiting

### Git Workflow
```powershell
# Before committing
git status
# Ensure .env and serviceAccountKey.json are NOT staged

git add .
git commit -m "Descriptive commit message"
git push
```

---

## Environment Management

### Multiple Environments

#### Development
```env
OPENAI_API_KEY="sk-dev-key"
FIREBASE_CREDENTIALS_PATH="./dev-serviceAccount.json"
OPENAI_MODEL="gpt-3.5-turbo"  # Cheaper for testing
```

#### Production
```env
OPENAI_API_KEY="sk-prod-key"
FIREBASE_CREDENTIALS_PATH="./prod-serviceAccount.json"
OPENAI_MODEL="gpt-4"
```

### Switching Environments
```powershell
# Copy environment-specific file
Copy-Item .env.dev .env  # For development
Copy-Item .env.prod .env  # For production
```

---

## Next Steps

1. ✅ Complete initial setup
2. ✅ Test basic functionality
3. ⬜ Add custom tools for your use case
4. ⬜ Populate knowledge base with relevant docs
5. ⬜ Build frontend integration (React Canvas)
6. ⬜ Implement authentication/authorization
7. ⬜ Add comprehensive error handling
8. ⬜ Create unit and integration tests
9. ⬜ Set up CI/CD pipeline
10. ⬜ Deploy to production environment

---

## Additional Resources

- **LangChain Docs**: https://python.langchain.com/docs/
- **OpenAI API Docs**: https://platform.openai.com/docs/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Firebase Docs**: https://firebase.google.com/docs/firestore
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

---

## Getting Help

- Check the README.md for overview
- Review spec kit files in `codex/` directory
- Search LangChain documentation
- Check OpenAI community forums
- Review Firebase support docs
