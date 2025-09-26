📌 Pull Request Template
🔖 Title

Clear and descriptive.
Example:

feat: add subscription renewal API

fix: resolve login token expiry issue

chore: update Dockerfile for production

📑 Description

Summary: Short explanation of what this PR does.

Context: Why this change is required.

Implementation Notes: Key technical details, approaches, or design decisions.

✅ Pre-Submission Checklist

 Code builds successfully

 Lint/format checks pass (eslint, prettier, flake8, pylint, checkstyle, etc.)

 Unit tests written & passing (≥90% coverage where applicable)

 Functional/integration tests written & passing (≥85% coverage where applicable)

 Secrets/tokens not exposed in code or config

 CI/CD pipeline green

 Documentation updated (README, API docs, comments)

 No breaking changes (or clearly documented in Migration Notes)

🧪 Testing Evidence

Attach proof of validation:

✅ Logs / Console output (test runs, build output)

✅ Screenshots (UI changes, API Postman tests, Swagger outputs)

✅ Curl/Postman examples (for APIs)

📂 Related Issues / Tickets

Link to JIRA / GitHub Issue / Task ID.
Example:

Fixes #123

JIRA-456

📌 Type of Change

 ✨ Feature

 🐞 Bug Fix

 🛠️ Refactor / Optimization

 🧹 Chore (docs, CI/CD, configs)

 🔒 Security Fix

🔄 Dependencies

Does this PR depend on any other PR/module?

Example: Depends on PR #45 (wallet-service)

👀 Reviewer Notes

Anything specific for reviewers to check (logic, edge cases, architecture).

📌 Tech-Specific Checks (Fill what applies)

Node.js/React/Next.js:

 npm run lint & npm run test pass

 Environment variables validated (.env.example updated)

Java/Spring Boot:

 mvn clean install or gradle build successful

 Checkstyle / PMD / SonarQube analysis passed

Python (Flask/FastAPI/Django):

 pytest or unittest pass

 flake8 / pylint checks pass

Solidity/Web3:

 truffle test / hardhat test pass

 Contracts audited for gas efficiency & security

CI/CD / Infra:

 Docker build successful (docker build .)

 K8s manifests / Helm charts updated if needed

⚠️ Reminder: PRs without filling mandatory sections (Description, Checklist, Testing Evidence) may be sent back for rework.
