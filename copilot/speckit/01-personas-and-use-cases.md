# Personas & Use Cases

## Primary Personas

### 1. Offensive Security Consultant (Alice)
- Runs scoped web/mobile/cloud engagements for clients.
- Needs fast answers about attack paths, remediation guidance, and prior engagement state.
- Works primarily from CLI tooling with intermittent GUI use.

### 2. Security Program Manager (Marco)
- Oversees multiple engagements and cares about repeatability, knowledge capture, and auditability.
- Reviews engagement history to ensure compliance and to inform reports.
- Less technical day-to-day but needs reliable summaries and replay ability.

## Key User Journeys

1. **Kick off a new engagement**
   - Configure .env, load keys, seed the knowledge base with customer-specific intel, and validate Firebase connectivity.
2. **Ask tactical vulnerability questions**
   - Consultant inquires about likely vulnerabilities or mitigation guidance; agent answers using GPT-4 grounded by ChromaDB excerpts.
3. **Simulate a vulnerability scan**
   - User triggers the ulnerability_scan tool to surface pre-defined findings that stand in for actual scanner output while prototyping.
4. **Retrieve engagement memory**
   - User runs get_engagement_context to review prior actions, commands, and responses captured in Firestore.
5. **Extend tooling**
   - Developer registers a new LangChain Tool that wraps an internal script or API and exposes it to the agent.

## Non-Goals (Initial Phase)
- Building a production-grade reporting UI.
- Executing actual intrusive scans from this backend (simulated only for now).
- Multi-tenant access control; assume single-team control of the backend.
