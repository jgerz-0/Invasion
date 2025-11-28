# Delivery Plan & Milestones

## Phase 0 ? Spec & Environment (current)
- Finalize Copilot SpecKit (this folder).
- Confirm Python 3.8+ and virtualenv baseline.
- Document credential handling and security assumptions.

## Phase 1 ? Prototype Hardening
- Implement validation around Firestore initialization failures (retry/backoff stubs).
- Add structured logging wrappers instead of raw print.
- Expand sample knowledge ingestion utilities (load from files/URLs).
- Provide CLI flags for engagement name & knowledge seeding.

## Phase 2 ? Tooling Expansion
- Add wrappers for real scanners (Nmap, nuclei) or integrate with existing APIs.
- Implement result normalization so new tools return consistent JSON payloads.
- Build metadata-driven prompts so agent knows when to call which tool.

## Phase 3 ? API & Automation
- Expose REST or gRPC interface for frontend integration.
- Gate requests with API tokens / authn to prep for multi-user access.
- Add job queue for long-running scans; persist state in Firestore or alternative DB.

## Backlog / Future Considerations
- Knowledge lifecycle management (versioning, cleanup, differential sync).
- Role-based access control around engagement data.
- Observability stack (structured logs, metrics, tracing) once deployed beyond CLI.
- Packaging into Docker image or serverless function for consistent deployments.

## Open Questions
1. Do we require on-premise variant without OpenAI (e.g., Azure OpenAI, local LLM)?
2. Should RAG sources be multi-format (PDF, Markdown) or limited to plaintext at launch?
3. Is there a need for automated report generation from engagement history in early releases?
