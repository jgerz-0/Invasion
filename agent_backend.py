"""
PenTest AI Agent Backend
========================
This module implements a PenTest AI Agent using OpenAI's API, LangChain for orchestration,
ChromaDB for RAG (Retrieval-Augmented Generation), and Firebase/Firestore for persistent memory.

Core Components:
- LLM Integration (OpenAI GPT-4)
- RAG System (ChromaDB vector store)
- Persistent Memory (Firestore)
- Tool Execution Framework
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Environment and Configuration
from dotenv import load_dotenv

# OpenAI and LangChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory

# Vector Store for RAG
from langchain_community.vectorstores import Chroma

# Firebase for persistent storage
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()


class PenTestAgent:
    """
    Main PenTest AI Agent class that orchestrates LLM, RAG, and persistent memory.
    """
    
    def __init__(self):
        """Initialize the PenTest Agent with all required components."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4")
        self.chroma_persist_dir = os.getenv("CHROMADB_PERSIST_DIR", "./chroma_db")
        
        # Initialize components
        self.llm = None
        self.embeddings = None
        self.vector_store = None
        self.db = None
        self.memory = None
        self.agent_executor = None
        
        # Initialize the agent
        self._initialize_llm()
        self._initialize_rag()
        self._initialize_firestore()
        self._initialize_tools()
        self._initialize_agent()
    
    def _initialize_llm(self):
        """Initialize the OpenAI LLM."""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key
        )
        
        print(f"✓ LLM initialized: {self.model_name}")
    
    def _initialize_rag(self):
        """Initialize the RAG system with ChromaDB."""
        try:
            # Create or load the vector store
            self.vector_store = Chroma(
                collection_name="pentest_knowledge",
                embedding_function=self.embeddings,
                persist_directory=self.chroma_persist_dir
            )
            print(f"✓ RAG system initialized with ChromaDB at {self.chroma_persist_dir}")
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB: {e}")
            self.vector_store = None
    
    def _initialize_firestore(self):
        """Initialize Firebase/Firestore for persistent memory."""
        try:
            if not firebase_admin._apps:
                if os.path.exists(self.firebase_credentials_path):
                    cred = credentials.Certificate(self.firebase_credentials_path)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    print("✓ Firestore initialized for persistent memory")
                else:
                    print(f"Warning: Firebase credentials not found at {self.firebase_credentials_path}")
                    self.db = None
            else:
                self.db = firestore.client()
        except Exception as e:
            print(f"Warning: Could not initialize Firestore: {e}")
            self.db = None
    
    def _initialize_tools(self):
        """Initialize the tools available to the agent."""
        self.tools = []
        
        # RAG Knowledge Retrieval Tool
        if self.vector_store:
            def knowledge_search(query: str) -> str:
                """Search the knowledge base for relevant penetration testing information."""
                try:
                    docs = self.vector_store.similarity_search(query, k=3)
                    if docs:
                        results = "\n\n".join([doc.page_content for doc in docs])
                        return f"Knowledge Base Results:\n{results}"
                    return "No relevant information found in knowledge base."
                except Exception as e:
                    return f"Error searching knowledge base: {str(e)}"
            
            self.tools.append(Tool(
                name="knowledge_search",
                func=knowledge_search,
                description="Search the penetration testing knowledge base for techniques, vulnerabilities, and best practices."
            ))
        
        # Mock Vulnerability Scanner Tool
        def vulnerability_scan(target: str) -> str:
            """Simulate a vulnerability scan on a target."""
            return f"""
Vulnerability Scan Results for {target}:
- Open Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)
- Detected Services: OpenSSH 8.2, Apache 2.4.41
- Potential Vulnerabilities: CVE-2021-3156 (sudo vulnerability)
- Risk Level: Medium
"""
        
        self.tools.append(Tool(
            name="vulnerability_scan",
            func=vulnerability_scan,
            description="Perform a simulated vulnerability scan on a target IP or domain."
        ))
        
        # Engagement Memory Tool
        def get_engagement_context(engagement_name: str) -> str:
            """Retrieve context and history for a specific engagement."""
            if self.db:
                try:
                    doc_ref = self.db.collection('engagements').document(engagement_name)
                    doc = doc_ref.get()
                    if doc.exists:
                        data = doc.to_dict()
                        return f"Engagement Context:\n{json.dumps(data, indent=2)}"
                    return f"No existing data for engagement: {engagement_name}"
                except Exception as e:
                    return f"Error retrieving engagement data: {str(e)}"
            return "Firestore not available"
        
        self.tools.append(Tool(
            name="get_engagement_context",
            func=get_engagement_context,
            description="Retrieve historical context and data for a specific penetration testing engagement."
        ))
        
        print(f"✓ Initialized {len(self.tools)} tools")
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with tools and memory."""
        # Create the prompt template
        system_message = """You are an expert Penetration Testing AI Assistant. Your role is to help security professionals 
conduct penetration tests by providing guidance, executing scans, and maintaining engagement context.

You have access to tools for:
- Searching the penetration testing knowledge base
- Running vulnerability scans
- Retrieving engagement history and context

Always be thorough, professional, and security-conscious in your responses. When conducting tests, 
explain your reasoning and provide actionable recommendations.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        print("✓ Agent executor initialized")
    
    def handle_command(self, command: str, engagement_name: str) -> Dict[str, Any]:
        """
        Main entry point for processing user commands.
        
        Args:
            command: The user's input command or question
            engagement_name: The name of the current engagement for context
        
        Returns:
            A dictionary containing the response and metadata
        """
        try:
            # Add engagement context to the command
            enhanced_command = f"[Engagement: {engagement_name}] {command}"
            
            # Execute the agent
            result = self.agent_executor.invoke({"input": enhanced_command})
            
            # Save interaction to Firestore
            self._save_interaction(engagement_name, command, result['output'])
            
            return {
                "success": True,
                "response": result['output'],
                "engagement": engagement_name,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            error_msg = f"Error processing command: {str(e)}"
            print(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "engagement": engagement_name,
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_interaction(self, engagement_name: str, command: str, response: str):
        """Save the interaction to Firestore for persistent memory."""
        if self.db:
            try:
                doc_ref = self.db.collection('engagements').document(engagement_name)
                
                # Get existing data or create new
                doc = doc_ref.get()
                if doc.exists:
                    data = doc.to_dict()
                    interactions = data.get('interactions', [])
                else:
                    interactions = []
                
                # Add new interaction
                interactions.append({
                    'timestamp': datetime.now().isoformat(),
                    'command': command,
                    'response': response
                })
                
                # Update Firestore
                doc_ref.set({
                    'engagement_name': engagement_name,
                    'interactions': interactions,
                    'last_updated': datetime.now().isoformat()
                })
                
                print(f"✓ Saved interaction to Firestore for engagement: {engagement_name}")
            
            except Exception as e:
                print(f"Warning: Could not save to Firestore: {e}")
    
    def add_knowledge(self, documents: List[str], metadatas: Optional[List[Dict]] = None):
        """
        Add documents to the RAG knowledge base.
        
        Args:
            documents: List of text documents to add
            metadatas: Optional metadata for each document
        """
        if self.vector_store:
            try:
                self.vector_store.add_texts(
                    texts=documents,
                    metadatas=metadatas
                )
                print(f"✓ Added {len(documents)} documents to knowledge base")
            except Exception as e:
                print(f"Error adding documents to knowledge base: {e}")
        else:
            print("Vector store not initialized")


def main():
    """
    Example usage of the PenTest Agent.
    """
    print("=" * 60)
    print("PenTest AI Agent - Backend Initialization")
    print("=" * 60)
    
    # Initialize the agent
    agent = PenTestAgent()
    
    print("\n" + "=" * 60)
    print("Agent Ready!")
    print("=" * 60)
    
    # Example: Add some knowledge to the RAG system
    sample_knowledge = [
        "OWASP Top 10 includes SQL Injection, which allows attackers to interfere with database queries.",
        "Port scanning is typically done using tools like Nmap to discover open ports and services.",
        "XSS (Cross-Site Scripting) allows attackers to inject malicious scripts into web pages.",
    ]
    
    agent.add_knowledge(sample_knowledge)
    
    # Example: Handle a command
    response = agent.handle_command(
        command="What are common web application vulnerabilities?",
        engagement_name="demo-engagement-001"
    )
    
    print("\n" + "=" * 60)
    print("Example Response:")
    print("=" * 60)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
