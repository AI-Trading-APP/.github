# Workspace guide

This workspace holds multiple independent git repos (one per service:
`aitradingnode`, `ScreenerService`, `portfolioservice`, etc.). The workspace
root itself is not a git repo.

## Multi-session coordination protocol

Multiple Claude sessions work this workspace in parallel — one feature per
session, and often a fresh session per task to save tokens. Treat every session
as a separate teammate with no shared memory. The shared state lives on disk in
`.coordination/` and in each feature branch's git log. Follow this protocol.

### 1. Isolation — one worktree per feature (not per session)
Each feature gets its own git worktree + branch off `development`, in the
relevant repo:

```
git -C <repo> worktree add ../<repo>-feat-<name> -b feature/<name> development
```

The worktree persists on disk across sessions. A new session for the next task
just `cd`s back into that same worktree — branch, history, and uncommitted work
are all still there.

### 2. Branching & merge rules
- Branch off `development`. Name it `feature/<name>` (add `-session-a/-b` only
  when two sessions intentionally split one feature).
- A finished feature merges to **`development`** — never `main`.
- Before continuing work, `git rebase development` so you absorb other merged
  features early and hit conflicts small.

### 3. Collision check (do this BEFORE editing)
- Read `.coordination/locks.md`. If your feature needs files another active
  feature has claimed, **stop and tell the user** — that feature must merge to
  `development` first. Otherwise add your row and proceed.
- Release your row when your feature merges.

### 4. Resuming a feature in a new session (token-saving handoff)
- Every feature carries a committed `FEATURE.md` at the repo root **on its own
  branch**. Because it lives on the branch, it travels through the remote to any
  laptop or engineer who checks out that branch.
- On session start, read `FEATURE.md` **and** run
  `git -C <repo> log development..HEAD` on the feature branch. That is your full
  state — do NOT re-derive it from scratch.
- When you finish a task: update `FEATURE.md` (Done / Next / decisions / where
  to resume) and commit it on the feature branch, then end the session.
- On merge to `development`: move it to `docs/features/<name>.md` (archived
  history) so `development` root stays clean. Seed a new feature with:
  `cp .coordination/features/_TEMPLATE.md <repo>/FEATURE.md`.

Net effect: no mid-flight conflicts (separate worktrees), dependencies block at
the lock/merge gate, and each new session resumes from a small file + git log
instead of re-loading a whole feature's context.

<!-- sdlc-global-standard -->
## SDLC Standard (global)
This project follows the machine-wide SDLC standard in `~/.claude/commands/sdlc.md` and the templates in `~/.claude/templates/` (auto-synced into `specs/_templates/` by the SessionStart hook). See `~/.claude/CLAUDE.md` §7 — global is the hub: learnings proven here are promoted to global and adopted by all projects. Reference the standard; don't fork it.


---

## 7. Global Testing Expectations: Browser-Based End-to-End Functional Testing, Database Integrity & Hidden Defect Detection

### 7.1. Objective
Act as a Principal QA Automation Architect, Senior Full-Stack Engineer, Database Reliability Engineer, and Security Tester.

Design and implement a reusable, browser-based automated testing framework that validates application functionality end to end and detects defects across the frontend, backend, database, asynchronous processing, external integrations, security boundaries, and operational behavior.

The framework must prove that application changes work as intended, persist the correct data, preserve existing functionality, and do not introduce hidden defects.

Do not limit testing to browser screenshots, successful HTTP responses, or visible UI messages.

### 7.2. Inspect the Existing Application First
Before making code changes:
1. Inspect the repository structure, application architecture, frontend, backend, APIs, database schemas and migrations, authentication, authorization, background jobs, event queues, external integrations, and existing tests.
2. Identify the actual technology stack, available test frameworks, environment configuration, and supported test commands.
3. Identify critical user journeys and map each journey to its frontend actions, API calls, business rules, database changes, and side effects.
4. Identify existing test coverage, untested workflows, known limitations, and potential architectural risks.
5. Prepare a proposed implementation plan with prioritized gaps and acceptance criteria.

Do not invent APIs, database tables, business rules, or expected outcomes. Derive them from the codebase, documented requirements, migrations, and existing behavior. Flag any ambiguity for clarification.

### 7.3. Implement the Testing Framework
Build an automated framework that supports:
- Real-browser testing using Playwright (`npx playwright test`).
- UI interaction, navigation, form validation, session management, and responsive behavior.
- API request and response validation.
- Database assertions against the actual persisted state.
- Business rule and state-transition validation.
- Asynchronous processing and event-driven workflow verification.
- Integration failure, retry, timeout, and recovery testing.
- Regression testing for existing features.
- Security and tenant-isolation checks.
- Repeatable test data setup, cleanup, and environment isolation.
- Detailed execution reports with evidence and failure diagnostics.

### 7.4. Validate Every Critical Workflow at Multiple Layers
For every critical business action, verify the following:

**A. Browser/UI:**
- Correct page, component, data, and status are displayed.
- User input and validation rules behave correctly.
- Loading, success, empty, and error states are handled correctly.
- Duplicate clicks and repeated submissions do not cause unintended effects.

**B. API/Backend:**
- Correct endpoint, HTTP status, response structure, and business result.
- Authentication, authorization, and tenant boundaries are enforced.
- Business rules are applied consistently.
- Errors are not silently swallowed or converted into misleading success responses.

**C. Database:**
- Expected records are created, updated, or deleted.
- Unrelated records remain unchanged.
- Foreign-key relationships and required constraints remain valid.
- Amounts, quantities, identifiers, timestamps, and statuses are correct.
- Transactions are atomic where required.
- Duplicate, orphaned, or inconsistent records are detected.
- Database state matches the expected business outcome.

**D. Side Effects:**
- Expected events, audit logs, notifications, jobs, and integration calls occur.
- Unexpected side effects are identified.
- Retries and repeated requests do not create duplicate business transactions.
- Failed operations do not leave invalid partial state.
- Eventual consistency is validated within an explicitly defined timeout.

### 7.5. Build a Requirements-to-Tests Traceability System
For every feature or change, maintain:
- Requirement or issue identifier.
- Business rule and expected behavior.
- Preconditions and user permissions.
- Test scenario and test data.
- Browser steps.
- API assertions.
- Database assertions.
- Expected side effects.
- Negative and boundary scenarios.
- Regression coverage.
- Execution result and supporting evidence.

### 7.6. Detect Hidden and Silent Defects
Explicitly test for:
- UI success with failed or missing database persistence.
- API success with incorrect business data.
- Incorrect database updates despite a correct UI response.
- Swallowed exceptions and missing error logs.
- Incorrect status transitions and stale cached data.
- Duplicate requests, duplicate payments, and race conditions.
- Partial commits and failed rollback behavior.
- Broken relationships, orphan records, and unintended data mutations.
- Failed background jobs, lost events, and repeated event processing.
- Cross-tenant data leakage.

### 7.7. Database Validation and Safety Requirements
- Discover the actual database engine, schemas, migrations, and access mechanisms.
- Prefer read-only database credentials for test assertions.
- Use a dedicated test database or isolated test tenant for mutations.
- Never use production customer or payment data without explicit authorization.
- Never expose passwords, API keys, payment credentials, or tokens in logs.
- Use transactions, fixtures, or deterministic cleanup where supported.

### 7.8. Test Categories and Execution Strategy
Implement: Smoke, Functional, End-to-end, Database integrity, Negative, Regression, Integration, Security, Reliability, and Performance smoke tests.

### 7.9. Definition of Done
Complete only when framework is implemented, setup/execution is documented, critical journeys have automated browser tests, mutations have independent API & DB assertions, CI/CD is configured, and tests are executed with actual reported logs.

### 7.10. Strict 85% Line & Functional Coverage Mandate (JaCoCo, Pytest & Frontend)
Every backend service and frontend application must independently achieve >= 85% executable line coverage and >= 85% functional branch/mutation coverage:
- **Backend (Java / Spring Boot):** Enforced via JaCoCo (`mvn verify` / `jacoco:check`) with an independent >= 85% line and branch threshold per class. Zero aggregate masking.
- **Backend (Python / FastAPI):** Enforced via `pytest --cov --cov-fail-under=85` with branch coverage.
- **Frontend (React / Vite / Next.js):** Enforced via Vitest / Jest / Istanbul (`npm run test:coverage`) with >= 85% line and branch coverage.
- **Zero Cosmetic Mocks:** Unit tests must validate true functional branches, mutations, and error handling. Mocking business entities merely to inflate coverage without executing business rules is strictly prohibited.
