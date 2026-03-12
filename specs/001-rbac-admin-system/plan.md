# Implementation Plan: RBAC Admin System

**Branch**: `001-rbac-admin-system` | **Date**: 2026-03-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rbac-admin-system/spec.md`

## Summary

Build an enterprise-level RBAC (Role-Based Access Control) admin system with FastAPI backend and Vue 3 frontend. The system provides comprehensive user management, department/position organization, menu-based permission control, and audit logging. Primary approach: modular backend (routers/schemas/crud/models) with async SQLAlchemy 2.0, JWT authentication via middleware, Redis caching for sessions and captcha; modular frontend (views/api/store/components) with dynamic routing and permission-based rendering.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: 
- Backend: FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2, PyJWT, python-multipart, aioredis, loguru
- Frontend: Vue 3, Vite, Element Plus, axios, Pinia, Vue Router
**Storage**: MySQL 8 (primary database), Redis (cache, session, captcha)
**Testing**: Pytest (backend), Vitest (frontend)
**Target Platform**: Linux server (Docker containerized), modern browsers (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application (frontend + backend separation)
**Performance Goals**: <500ms API response time, 100 concurrent users, <200ms database queries
**Constraints**: JWT token expiration 2 hours, refresh token 7 days, image upload max 5MB, department tree max 10 levels
**Scale/Scope**: ~30 API endpoints, ~15 frontend pages, 9 database entities, 7 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- [x] **I. Technology Stack**: Backend (FastAPI + Python 3.11+ / Pydantic v2 / SQLAlchemy 2.0 async / Alembic), Frontend (Vue 3 + TypeScript / Vite / Element Plus / Pinia / Vue Router), Database (MySQL 8 + Redis)
- [x] **II. Code Quality**: Black + Ruff (backend) / ESLint + Prettier (frontend) configured, 100% type hints planned
- [x] **III. Testing**: Pytest (backend) / Vitest (frontend) tests planned, acceptance criteria defined before implementation
- [x] **IV. Security**: JWT + middleware authentication approach defined, secrets management planned
- [x] **V. Documentation & Deployment**: OpenAPI auto-generation verified, Docker + docker-compose setup planned

**Compliance Status**: All principles satisfied. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-rbac-admin-system/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── api-contracts.md # API endpoint specifications
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection and session
│   ├── dependencies.py         # Dependency injection
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py             # Base model with common fields
│   │   ├── user.py
│   │   ├── department.py
│   │   ├── position.py
│   │   ├── menu.py
│   │   ├── role.py
│   │   ├── user_role.py
│   │   ├── role_menu.py
│   │   ├── operation_log.py
│   │   └── login_log.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── common.py           # Common response schemas
│   │   ├── user.py
│   │   ├── department.py
│   │   ├── position.py
│   │   ├── menu.py
│   │   ├── role.py
│   │   ├── auth.py
│   │   └── log.py
│   ├── crud/                   # CRUD operations
│   │   ├── __init__.py
│   │   ├── base.py             # Base CRUD class
│   │   ├── user.py
│   │   ├── department.py
│   │   ├── position.py
│   │   ├── menu.py
│   │   ├── role.py
│   │   └── log.py
│   ├── routers/                # API routers
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── users.py            # User management
│   │   ├── departments.py      # Department management
│   │   ├── positions.py        # Position management
│   │   ├── menus.py            # Menu management
│   │   ├── roles.py            # Role management
│   │   ├── logs.py             # Audit logs
│   │   └── upload.py           # File upload
│   ├── middleware/             # Middleware components
│   │   ├── __init__.py
│   │   ├── auth.py             # JWT authentication middleware
│   │   ├── logging.py          # Request logging middleware
│   │   └── cors.py             # CORS configuration
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py         # Password hashing, JWT handling
│   │   ├── captcha.py          # Captcha generation
│   │   ├── redis_client.py     # Redis connection and operations
│   │   └── file_storage.py     # File upload handling
│   └── core/                   # Core functionality
│       ├── __init__.py
│       ├── security.py         # Security utilities
│       └── permissions.py      # Permission checking
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
├── pyproject.toml              # Black, Ruff configuration
└── Dockerfile

frontend/
├── src/
│   ├── main.ts                 # Application entry point
│   ├── App.vue                 # Root component
│   ├── api/                    # API service modules
│   │   ├── index.ts            # Axios instance configuration
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   ├── department.ts
│   │   ├── position.ts
│   │   ├── menu.ts
│   │   ├── role.ts
│   │   └── log.ts
│   ├── views/                  # Page components
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── system/             # System management pages
│   │   │   ├── user/
│   │   │   ├── department/
│   │   │   ├── position/
│   │   │   ├── menu/
│   │   │   └── role/
│   │   └── log/                # Audit log pages
│   │       ├── operation/
│   │       └── login/
│   ├── components/             # Reusable components
│   │   ├── layout/
│   │   │   ├── Sidebar.vue
│   │   │   ├── Header.vue
│   │   │   ├── Tabs.vue
│   │   │   └── Breadcrumb.vue
│   │   ├── common/
│   │   │   ├── TreeSelect.vue
│   │   │   └── PermissionButton.vue
│   │   └── upload/
│   │       └── ImageUpload.vue
│   ├── store/                  # Pinia stores
│   │   ├── index.ts
│   │   ├── user.ts
│   │   ├── permission.ts
│   │   └── app.ts              # App state (sidebar, tabs)
│   ├── router/                 # Vue Router configuration
│   │   ├── index.ts
│   │   └── routes.ts           # Route definitions
│   ├── utils/                  # Utility functions
│   │   ├── auth.ts             # Token management
│   │   ├── permission.ts       # Permission checking
│   │   └── request.ts          # HTTP request wrapper
│   ├── types/                  # TypeScript type definitions
│   │   └── index.ts
│   └── assets/                 # Static assets
│       └── styles/
├── public/
├── vite.config.ts
├── tsconfig.json
├── package.json
├── .eslintrc.js
├── .prettierrc
└── Dockerfile

docker-compose.yml
.env.example
README.md
```

**Structure Decision**: Web application (Option 2) selected due to frontend + backend separation requirement. Backend follows FastAPI modular architecture (routers/schemas/crud/models pattern), frontend follows Vue 3 composition API with Pinia state management. Both backend and frontend are containerized with Docker.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitutional principles are satisfied by the proposed architecture.