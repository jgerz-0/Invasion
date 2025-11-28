# PenTest AI Agent Backend

A sophisticated Penetration Testing AI Agent built with Python, OpenAI's API, LangChain, ChromaDB for RAG (Retrieval-Augmented Generation), and Firebase/Firestore for persistent memory.

## 🎯 Overview

This backend system provides an intelligent AI agent that assists security professionals in conducting penetration tests by:
- Leveraging LLM capabilities for intelligent decision-making
- Using RAG to access a knowledge base of penetration testing techniques
- Maintaining persistent memory of engagement history via Firestore
- Executing various security tools and providing actionable insights

## 🏗️ Architecture

### Core Components

1. **LLM Integration** - OpenAI GPT-4 for natural language understanding and generation
2. **RAG System** - ChromaDB vector store for semantic search over security knowledge
3. **Persistent Memory** - Firebase/Firestore for engagement tracking and history
4. **Tool Framework** - Extensible tool system for security operations

### Key Features

- ✅ Command processing with context awareness
- ✅ Knowledge base retrieval for penetration testing techniques
- ✅ Simulated vulnerability scanning
- ✅ Engagement history and context management
- ✅ Conversation memory within sessions
- ✅ Persistent storage across sessions

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Firebase project with Firestore enabled ([Setup guide](https://firebase.google.com/docs/firestore/quickstart))

### Step 1: Clone and Navigate

```bash
cd c:\Users\User\Invasion
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate the environment
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   OPENAI_API_KEY="your-actual-openai-api-key"
   FIREBASE_CREDENTIALS_PATH="./serviceAccountKey.json"
   OPENAI_MODEL="gpt-4"
   CHROMADB_PERSIST_DIR="./chroma_db"
   ```

### Step 5: Setup Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Navigate to **Project Settings** → **Service Accounts**
4. Click **Generate New Private Key**
5. Save the downloaded JSON file as `serviceAccountKey.json` in the project root

### Step 6: Run the Agent

```powershell
# Make sure your virtual environment is activated
.\venv\Scripts\activate

# Run the agent
python agent_backend.py
```

## 📁 Project Structure

```
Invasion/
├── venv/                      # Virtual environment (generated)
├── chroma_db/                 # ChromaDB persistence directory (generated)
├── agent_backend.py           # Main agent implementation
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from .env.example)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── serviceAccountKey.json    # Firebase credentials (not in git)
└── README.md                 # This file
```

## 🔧 Usage

### Basic Example

```python
from agent_backend import PenTestAgent

# Initialize the agent
agent = PenTestAgent()

# Add knowledge to the RAG system
knowledge_docs = [
    "SQL Injection allows attackers to interfere with database queries...",
    "Cross-Site Scripting (XSS) enables injection of malicious scripts...",
]
agent.add_knowledge(knowledge_docs)

# Process a command
response = agent.handle_command(
    command="What vulnerabilities should I check for in a web application?",
    engagement_name="client-webapp-pentest-2025"
)

print(response)
```

### API Response Format

```json
{
  "success": true,
  "response": "Based on the OWASP Top 10, you should check for...",
  "engagement": "client-webapp-pentest-2025",
  "timestamp": "2025-11-29T10:30:00"
}
```

## 🛠️ Available Tools

The agent comes with three built-in tools:

1. **knowledge_search** - Search the penetration testing knowledge base
2. **vulnerability_scan** - Perform simulated vulnerability scans
3. **get_engagement_context** - Retrieve engagement history from Firestore

### Extending with Custom Tools

```python
from langchain.tools import Tool

def custom_tool(input_param: str) -> str:
    """Your custom tool implementation."""
    return f"Result for {input_param}"

tool = Tool(
    name="custom_tool_name",
    func=custom_tool,
    description="Description of what your tool does"
)

agent.tools.append(tool)
```

## 📊 Data Storage

### ChromaDB (Vector Store)
- Location: `./chroma_db/` (configurable via `CHROMADB_PERSIST_DIR`)
- Purpose: Stores embeddings for RAG knowledge retrieval
- Persistence: Automatic on disk

### Firestore (Engagement Memory)
- Collection: `engagements`
- Document ID: `engagement_name`
- Structure:
  ```json
  {
    "engagement_name": "string",
    "interactions": [
      {
        "timestamp": "ISO-8601",
        "command": "string",
        "response": "string"
      }
    ],
    "last_updated": "ISO-8601"
  }
  ```

## 🔐 Security Considerations

- **Never commit** `.env` or `serviceAccountKey.json` to version control
- Store API keys securely and rotate them regularly
- Use Firebase security rules to restrict Firestore access
- Run the agent in a secure, isolated environment
- Ensure proper authentication when exposing as an API

## 🐛 Troubleshooting

### Import Errors
These are expected before installing dependencies. Run:
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Firebase Connection Issues
- Verify `serviceAccountKey.json` path in `.env`
- Ensure Firestore is enabled in Firebase Console
- Check Firebase credentials have proper permissions

### ChromaDB Persistence Issues
- Ensure the `CHROMADB_PERSIST_DIR` directory is writable
- Check disk space availability

## 📝 Next Steps

1. **Install Dependencies**: Activate venv and run `pip install -r requirements.txt`
2. **Configure Credentials**: Set up `.env` with your OpenAI and Firebase keys
3. **Test the Agent**: Run `python agent_backend.py` to verify setup
4. **Add Knowledge**: Populate the RAG system with your security knowledge base
5. **Build Frontend**: Integrate with your React Canvas UI
6. **Deploy**: Consider containerization (Docker) for production deployment

## 📚 Dependencies

- `openai` - OpenAI API client
- `langchain` - LLM orchestration framework
- `langchain-openai` - OpenAI integration for LangChain
- `langchain-community` - Community tools and integrations
- `chromadb` - Vector database for RAG
- `python-dotenv` - Environment variable management
- `firebase-admin` - Firebase/Firestore SDK
- `requests` - HTTP library
- `pydantic` - Data validation

## 📄 License

This is a specification kit for building a PenTest AI Agent. Customize according to your needs.

## 🤝 Contributing

This is a starter template. Extend it with:
- Additional security tools integration
- Enhanced RAG capabilities
- Custom vulnerability scanners
- Reporting and visualization features
- API endpoints for frontend integration

---

**Built with ❤️ for the cybersecurity community**
