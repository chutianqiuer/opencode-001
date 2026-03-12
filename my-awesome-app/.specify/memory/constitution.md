<!--
=============================================================================
SYNC IMPACT REPORT
=============================================================================
Version Change: N/A → 1.0.0 (Initial Creation)

Modified Principles: N/A (Initial version)

Added Sections:
  - Core Principles (5 principles)
    - I. Technology Stack Standards
    - II. Code Quality & Type Safety
    - III. Testing Requirements
    - IV. Security & Authentication
    - V. Documentation & Deployment
  - Development Workflow
  - Governance

Removed Sections: N/A (Initial version)

Templates Requiring Updates:
  - .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section references principles)
  - .specify/templates/spec-template.md: ✅ Compatible (Acceptance Criteria aligns with Principle III)
  - .specify/templates/tasks-template.md: ✅ Compatible (Test tasks align with Principle III)

Follow-up TODOs: None

Rationale for MINOR version (1.0.0):
  - Initial constitution creation
  - No prior version to compare
  - Establishes baseline governance for the project
=============================================================================
-->

# my-awesome-app Constitution

## Core Principles

### I. Technology Stack Standards

The project MUST adhere to the following technology stack without deviation:

**Backend**:
- Framework: FastAPI with Python 3.11+
- Data Validation: Pydantic v2 (strict mode required)
- ORM: SQLAlchemy 2.0 async
- Database Migrations: Alembic

**Frontend**:
- Framework: Vue 3 with TypeScript
- Build Tool: Vite
- UI Library: Element Plus
- State Management: Pinia
- Routing: Vue Router

**Database & Cache**:
- Primary Database: MySQL 8
- Cache & Session: Redis

**Rationale**: Standardizing the technology stack ensures consistency across the codebase, reduces learning curve for new developers, and enables efficient debugging and maintenance. These technologies are mature, well-documented, and have strong community support.

### II. Code Quality & Type Safety

All code MUST meet the following quality standards:

**Code Formatting & Linting**:
- Backend: Black (formatter) + Ruff (linter)
- Frontend: ESLint + Prettier
- All linting rules MUST pass before merge

**Type Safety**:
- 100% type hints required for all Python code
- TypeScript strict mode enabled
- No `any` types without explicit justification

**Rationale**: Consistent code formatting and strict type safety reduce bugs, improve code readability, and enable better IDE support. Type hints serve as inline documentation and catch errors at development time rather than runtime.

### III. Testing Requirements

Testing is NON-NEGOTIABLE and MUST follow these requirements:

**Testing Frameworks**:
- Backend: Pytest
- Frontend: Vitest

**Coverage Requirements**:
- Every module MUST have corresponding unit tests
- New features MUST include tests that pass acceptance criteria
- Bug fixes MUST include regression tests

**Test-Driven Development**:
- All implementations MUST satisfy SPEC acceptance criteria before coding
- Tests define the contract; implementation fulfills it

**Rationale**: Comprehensive testing ensures code reliability, facilitates refactoring, and serves as living documentation. The "acceptance criteria first" approach prevents scope creep and ensures features meet requirements.

### IV. Security & Authentication

Security MUST NOT be compromised for convenience:

**Authentication**:
- Method: JWT (JSON Web Tokens)
- Implementation: Middleware-based authentication
- Token refresh: Required for long sessions

**Security Practices**:
- Secrets MUST NEVER be committed to the repository
- Environment variables for sensitive configuration
- Input validation on all API endpoints
- SQL injection prevention via ORM

**Rationale**: Security breaches can cause significant damage. JWT with middleware provides a scalable, stateless authentication mechanism suitable for modern web applications.

### V. Documentation & Deployment

Documentation and deployment MUST be automated:

**API Documentation**:
- OpenAPI specification auto-generated from FastAPI
- Swagger UI accessible for API exploration
- All endpoints MUST have descriptive summaries and examples

**Deployment**:
- Containerization: Docker
- Orchestration: docker-compose
- Environment configuration via docker-compose.yml or .env files

**Rationale**: Auto-generated documentation stays synchronized with code. Docker ensures consistent environments across development, testing, and production, eliminating "works on my machine" issues.

## Development Workflow

### Branch Strategy

- Feature branches: `feature/###-description`
- Bug fix branches: `fix/###-description`
- Release branches: `release/vX.Y.Z`

### Code Review Requirements

1. All changes MUST go through pull request review
2. At least one approval required before merge
3. All CI checks MUST pass (lint, type-check, test)
4. No force pushes to main branch

### Acceptance Criteria First

Before writing any implementation code:
1. Review SPEC acceptance criteria thoroughly
2. Write tests that verify acceptance criteria
3. Ensure tests fail (red phase of TDD)
4. Implement code to pass tests (green phase)
5. Refactor while maintaining test coverage

## Governance

### Amendment Procedure

1. Propose amendment with clear rationale
2. Document impact on existing code and processes
3. Update constitution with version increment
4. Propagate changes to dependent templates and documentation

### Versioning Policy

- **MAJOR**: Backward incompatible governance or principle removals/redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- All pull requests MUST verify compliance with constitution
- Complexity beyond defined standards MUST be justified in documentation
- Quarterly review of constitution relevance and updates

**Version**: 1.0.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12