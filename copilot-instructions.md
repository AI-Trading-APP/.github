# AI-Trading-APP — Workspace Rules

- Follow `AGENTS.md` and `CLAUDE.md`.
- Strict phase gating: Phase 1 design & impact requires owner approval before Phase 2 implementation.
- Multi-layer testing: Browser/UI, API/Backend, Database state (PostgreSQL / TimescaleDB), Side effects.
- Strict 85% line and branch coverage per microservice (JaCoCo for Java, pytest for Python, Vitest for Node).
- All PRs target `development`. Protected branches are write-only via PR.
