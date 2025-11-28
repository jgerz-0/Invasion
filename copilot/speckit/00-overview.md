# PenTest AI Agent ? SpecKit Overview

## Mission
Deliver an AI-driven penetration testing backend that streamlines reconnaissance insight generation, connects to a curated knowledge base, and captures engagement memory so security teams can iterate faster without losing context.

## Problem Statement
Security consultants juggle research, context management, and tooling orchestration during engagements. Manual context switching slows analysis and makes it difficult to reuse findings in future engagements. We need a backend assistant that can answer situational questions, recall prior steps, and simulate tool output while remaining extensible.

## Product Objectives
- Provide a conversational command surface backed by GPT-4 with deterministic guardrails.
- Support Retrieval-Augmented Generation via ChromaDB to ground answers in vetted penetration testing knowledge.
- Persist engagement history in Firestore so investigators can resume work with full context.
- Offer an extensible tool catalog (search, simulated scans, context fetch) with hooks for future tooling.
- Remain deployable in secure, air-gapped environments once dependencies are satisfied.

## Success Metrics
- <2 minutes to onboard a new engagement (configure .env, load keys, run agent).
- ?90% of user prompts resolved by RAG-backed LLM without requiring manual research.
- Firestore records at least 95% of commands issued per engagement with timestamps.
- New tool integrations can be added with ?50 lines of glue code each.

## Constraints & Assumptions
- Python 3.8+ environment with outbound network for OpenAI and Firebase.
- Users manage their own credentials and secrets; repo must remain secret-free.
- Initial deployment targets CLI/server execution; API/GUI layers are future work.

## References
- README.md ? project overview & setup instructions.
- agent_backend.py ? current prototype implementation.
- requirements.txt / .env.example ? dependency and configuration templates.
