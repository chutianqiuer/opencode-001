# Tasks: RBAC Admin System

**Input**: Design documents from `/specs/001-rbac-admin-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Per Constitution III (Testing Requirements), every module MUST have corresponding unit tests. Tests are MANDATORY - they define the contract before implementation.

**Constitution Compliance**: All tasks MUST adhere to `.specify/memory/constitution.md`:
- Technology stack standards (Principle I)
- Code quality & type safety (Principle II)
- Testing requirements (Principle III) - NON-NEGOTIABLE
- Security & authentication (Principle IV)
- Documentation & deployment (Principle V)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Priority Order**: Backend APIs first (US1-US7), then Frontend interactions (US1-US7).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`
- Backend models: `backend/app/models/`
- Backend schemas: `backend/app/schemas/`
- Backend CRUD: `backend/app/crud/`
- Backend routers: `backend/app/routers/`
- Frontend views: `frontend/src/views/`
- Frontend api: `frontend/src/api/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and initialize dependencies

### Backend Setup

- [ ] T001 Create backend project structure with directories: models/, schemas/, crud/, routers/, middleware/, utils/, core/
- [ ] T002 Initialize Python project with requirements.txt including FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, PyJWT, python-multipart, redis, loguru, passlib
- [ ] T003 [P] Configure Black and Ruff in backend/pyproject.toml
- [ ] T004 [P] Create backend/app/config.py for environment configuration management
- [ ] T005 [P] Create backend/app/database.py for async database connection with SQLAlchemy 2.0
- [ ] T006 [P] Create backend/app/dependencies.py for dependency injection

### Frontend Setup

- [ ] T007 Create frontend project structure with directories: views/, api/, store/, components/, router/, utils/, types/, assets/
- [ ] T008 Initialize Vue 3 project with package.json including Vue 3, TypeScript, Vite, Element Plus, axios, Pinia, Vue Router
- [ ] T009 [P] Configure ESLint and Prettier in frontend/.eslintrc.js and frontend/.prettierrc
- [ ] T010 [P] Create frontend/vite.config.ts with proxy configuration for API
- [ ] T011 [P] Create frontend/tsconfig.json with strict mode enabled

### Docker & Infrastructure

- [ ] T012 Create docker-compose.yml with services: backend, frontend, mysql, redis
- [ ] T013 [P] Create backend/Dockerfile
- [ ] T014 [P] Create frontend/Dockerfile
- [ ] T015 [P] Create .env.example with all required environment variables
- [ ] T016 Create README.md with project overview and quick start instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models (Base)

- [ ] T017 Create backend/app/models/base.py with common fields (id, created_at, updated_at, deleted_at)
- [ ] T018 [P] Create backend/app/schemas/common.py with ApiResponse and PageResponse schemas
- [ ] T019 [P] Create backend/app/crud/base.py with generic CRUD base class

### Core Infrastructure

- [ ] T020 Create backend/app/utils/security.py for password hashing (bcrypt) and JWT token generation/verification
- [ ] T021 [P] Create backend/app/utils/redis_client.py for Redis connection and operations
- [ ] T022 [P] Create backend/app/utils/captcha.py for graphical captcha generation using PIL
- [ ] T023 [P] Create backend/app/utils/file_storage.py for file upload handling with local storage interface
- [ ] T024 Create backend/app/core/permissions.py for permission checking utilities
- [ ] T025 Create backend/app/middleware/auth.py for JWT authentication middleware
- [ ] T026 [P] Create backend/app/middleware/logging.py for request logging with loguru
- [ ] T027 [P] Create backend/app/middleware/cors.py for CORS configuration

### Alembic Migrations Setup

- [ ] T028 Initialize Alembic in backend/ with `alembic init alembic`
- [ ] T029 Configure backend/alembic/env.py for async SQLAlchemy support

### Frontend Core

- [ ] T030 Create frontend/src/api/index.ts with axios instance and interceptors
- [ ] T031 [P] Create frontend/src/utils/auth.ts for token storage and management
- [ ] T032 [P] Create frontend/src/utils/request.ts for HTTP request wrapper
- [ ] T033 [P] Create frontend/src/utils/permission.ts for permission checking utilities
- [ ] T034 Create frontend/src/types/index.ts with TypeScript interfaces for all entities
- [ ] T035 Create frontend/src/store/index.ts with Pinia setup
- [ ] T036 [P] Create frontend/src/store/user.ts for user state management
- [ ] T037 [P] Create frontend/src/store/permission.ts for permission state management
- [ ] T038 [P] Create frontend/src/store/app.ts for app state (sidebar, tabs)
- [ ] T039 Create frontend/src/router/index.ts with Vue Router setup and route guards
- [ ] T040 Create frontend/src/App.vue as root component
- [ ] T041 Create frontend/src/main.ts as application entry point

### Main Application Entry

- [ ] T042 Create backend/app/main.py with FastAPI app initialization, middleware registration, and router inclusion

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP - Backend

**Goal**: Implement secure user login with JWT authentication and captcha verification

**Independent Test**: Access login endpoint, verify captcha generation, login with valid credentials, receive JWT token, verify protected endpoints require authentication

### Tests for User Story 1 (Backend)

- [ ] T043 [P] [US1] Create backend/tests/unit/test_security.py for password hashing and JWT tests
- [ ] T044 [P] [US1] Create backend/tests/unit/test_captcha.py for captcha generation tests
- [ ] T045 [P] [US1] Create backend/tests/api/test_auth.py for authentication endpoint tests

### Models & Schemas for US1

- [ ] T046 [P] [US1] Create backend/app/models/user.py with User model
- [ ] T047 [P] [US1] Create backend/app/models/login_log.py with LoginLog model
- [ ] T048 [P] [US1] Create backend/app/schemas/auth.py with LoginRequest, LoginResponse, CaptchaResponse, TokenRefresh schemas
- [ ] T049 [P] [US1] Create backend/app/schemas/user.py with UserCreate, UserUpdate, UserResponse schemas

### CRUD & Router for US1

- [ ] T050 [US1] Create backend/app/crud/user.py with user CRUD operations
- [ ] T051 [US1] Create backend/app/crud/log.py with login log CRUD operations
- [ ] T052 [US1] Create backend/app/routers/auth.py with login, logout, refresh, captcha, user info endpoints
- [ ] T053 [US1] Register auth router in backend/app/main.py

### Database Migration for US1

- [ ] T054 [US1] Create Alembic migration for users table
- [ ] T055 [US1] Create Alembic migration for login_logs table
- [ ] T056 [US1] Create seed data script for default super admin user

**Checkpoint**: Backend authentication fully functional - can test login with Postman/curl

---

## Phase 4: User Story 2 - Department Management (Priority: P2) - Backend

**Goal**: Implement tree-structured department hierarchy with CRUD operations

**Independent Test**: Create department tree, verify parent-child relationships, test department dropdown endpoint, prevent deletion of departments with children/users

### Tests for User Story 2 (Backend)

- [ ] T057 [P] [US2] Create backend/tests/unit/test_department.py for department model tests
- [ ] T058 [P] [US2] Create backend/tests/api/test_departments.py for department API tests

### Models & Schemas for US2

- [ ] T059 [P] [US2] Create backend/app/models/department.py with Department model (self-referential parent_id)
- [ ] T060 [P] [US2] Create backend/app/schemas/department.py with DepartmentCreate, DepartmentUpdate, DepartmentTree schemas

### CRUD & Router for US2

- [ ] T061 [US2] Create backend/app/crud/department.py with tree query using recursive CTE
- [ ] T062 [US2] Create backend/app/routers/departments.py with CRUD and tree dropdown endpoints
- [ ] T063 [US2] Register departments router in backend/app/main.py

### Database Migration for US2

- [ ] T064 [US2] Create Alembic migration for departments table

**Checkpoint**: Department management API fully functional

---

## Phase 5: User Story 3 - Position Management (Priority: P3) - Backend

**Goal**: Implement job position CRUD with status toggle and dropdown list

**Independent Test**: Create positions, toggle status, verify dropdown shows only active positions

### Tests for User Story 3 (Backend)

- [ ] T065 [P] [US3] Create backend/tests/unit/test_position.py for position model tests
- [ ] T066 [P] [US3] Create backend/tests/api/test_positions.py for position API tests

### Models & Schemas for US3

- [ ] T067 [P] [US3] Create backend/app/models/position.py with Position model
- [ ] T068 [P] [US3] Create backend/app/schemas/position.py with PositionCreate, PositionUpdate, PositionResponse schemas

### CRUD & Router for US3

- [ ] T069 [US3] Create backend/app/crud/position.py with position CRUD operations
- [ ] T070 [US3] Create backend/app/routers/positions.py with CRUD, status toggle, and dropdown endpoints
- [ ] T071 [US3] Register positions router in backend/app/main.py

### Database Migration for US3

- [ ] T072 [US3] Create Alembic migration for positions table

**Checkpoint**: Position management API fully functional

---

## Phase 6: User Story 4 - Menu & Permission Management (Priority: P4) - Backend

**Goal**: Implement tree-structured menu hierarchy with permission codes for button-level control

**Independent Test**: Create menu tree with directories, menus, and buttons, verify permission codes are stored correctly

### Tests for User Story 4 (Backend)

- [ ] T073 [P] [US4] Create backend/tests/unit/test_menu.py for menu model tests
- [ ] T074 [P] [US4] Create backend/tests/api/test_menus.py for menu API tests

### Models & Schemas for US4

- [ ] T075 [P] [US4] Create backend/app/models/menu.py with Menu model (type: directory/menu/button)
- [ ] T076 [P] [US4] Create backend/app/schemas/menu.py with MenuCreate, MenuUpdate, MenuTree schemas

### CRUD & Router for US4

- [ ] T077 [US4] Create backend/app/crud/menu.py with tree query and permission code handling
- [ ] T078 [US4] Create backend/app/routers/menus.py with CRUD and tree endpoints
- [ ] T079 [US4] Register menus router in backend/app/main.py

### Database Migration for US4

- [ ] T080 [US4] Create Alembic migration for menus table
- [ ] T081 [US4] Create seed data script for default menu structure

**Checkpoint**: Menu management API fully functional

---

## Phase 7: User Story 5 - Role Management (Priority: P5) - Backend

**Goal**: Implement role CRUD with menu permission assignment

**Independent Test**: Create roles, assign menus via permission tree, verify role-menu relationships

### Tests for User Story 5 (Backend)

- [ ] T082 [P] [US5] Create backend/tests/unit/test_role.py for role model tests
- [ ] T083 [P] [US5] Create backend/tests/api/test_roles.py for role API tests

### Models & Schemas for US5

- [ ] T084 [P] [US5] Create backend/app/models/role.py with Role model
- [ ] T085 [P] [US5] Create backend/app/models/role_menu.py with RoleMenu junction table
- [ ] T086 [P] [US5] Create backend/app/schemas/role.py with RoleCreate, RoleUpdate, RoleResponse schemas

### CRUD & Router for US5

- [ ] T087 [US5] Create backend/app/crud/role.py with role CRUD and menu assignment
- [ ] T088 [US5] Create backend/app/routers/roles.py with CRUD, status toggle, and menu assignment endpoints
- [ ] T089 [US5] Register roles router in backend/app/main.py

### Database Migration for US5

- [ ] T090 [US5] Create Alembic migration for roles table
- [ ] T091 [US5] Create Alembic migration for role_menus junction table
- [ ] T092 [US5] Create seed data script for default roles

**Checkpoint**: Role management API fully functional

---

## Phase 8: User Story 6 - User Management (Priority: P6) - Backend

**Goal**: Implement user CRUD with role assignment, password reset, and avatar upload

**Independent Test**: Create users with department/position/role, reset password, upload avatar, toggle status

### Tests for User Story 6 (Backend)

- [ ] T093 [P] [US6] Create backend/tests/api/test_users.py for user management API tests
- [ ] T094 [P] [US6] Create backend/tests/api/test_upload.py for file upload tests

### Models & Schemas for US6

- [ ] T095 [P] [US6] Create backend/app/models/user_role.py with UserRole junction table
- [ ] T096 [P] [US6] Update backend/app/schemas/user.py with UserProfile, UserListResponse schemas

### CRUD & Router for US6

- [ ] T097 [US6] Update backend/app/crud/user.py with role assignment, password reset, profile update
- [ ] T098 [US6] Create backend/app/routers/users.py with CRUD, status toggle, reset password, profile endpoints
- [ ] T099 [US6] Create backend/app/routers/upload.py with avatar upload endpoint
- [ ] T100 [US6] Register users and upload routers in backend/app/main.py

### Database Migration for US6

- [ ] T101 [US6] Create Alembic migration for user_roles junction table

**Checkpoint**: User management API fully functional

---

## Phase 9: User Story 7 - Audit Logging (Priority: P7) - Backend

**Goal**: Implement operation log and login log with filtering and batch deletion

**Independent Test**: Perform operations, verify logs are recorded, test filtering and batch deletion

### Tests for User Story 7 (Backend)

- [ ] T102 [P] [US7] Create backend/tests/api/test_logs.py for log API tests

### Models & Schemas for US7

- [ ] T103 [P] [US7] Create backend/app/models/operation_log.py with OperationLog model
- [ ] T104 [P] [US7] Create backend/app/schemas/log.py with OperationLogResponse, LoginLogResponse schemas

### CRUD & Router for US7

- [ ] T105 [US7] Update backend/app/crud/log.py with operation log CRUD
- [ ] T106 [US7] Create backend/app/routers/logs.py with operation and login log endpoints
- [ ] T107 [US7] Register logs router in backend/app/main.py
- [ ] T108 [US7] Create operation log decorator in backend/app/utils/decorators.py for automatic logging
- [ ] T109 [US7] Apply operation log decorator to all CRUD endpoints

### Database Migration for US7

- [ ] T110 [US7] Create Alembic migration for operation_logs table

**Checkpoint**: All backend APIs complete - backend MVP ready

---

## Phase 10: User Story 1 - User Authentication (Priority: P1) - Frontend

**Goal**: Implement login page with captcha and JWT token management

**Independent Test**: Navigate to login page, enter credentials, receive token, redirect to dashboard, logout

### Layout Components

- [ ] T111 [P] [US1] Create frontend/src/components/layout/Sidebar.vue for navigation sidebar
- [ ] T112 [P] [US1] Create frontend/src/components/layout/Header.vue with user info and logout
- [ ] T113 [P] [US1] Create frontend/src/components/layout/Tabs.vue for tab navigation
- [ ] T114 [P] [US1] Create frontend/src/components/layout/Breadcrumb.vue for breadcrumb navigation

### API & Views for US1

- [ ] T115 [P] [US1] Create frontend/src/api/auth.ts with login, logout, refresh, captcha, userInfo methods
- [ ] T116 [US1] Create frontend/src/views/login/index.vue with captcha display and login form
- [ ] T117 [US1] Create frontend/src/views/dashboard/index.vue as landing page
- [ ] T118 [US1] Update frontend/src/router/routes.ts with login and dashboard routes
- [ ] T119 [US1] Implement route guard in frontend/src/router/index.ts for authentication check

**Checkpoint**: Frontend login flow complete - can log in and see dashboard

---

## Phase 11: User Story 2 - Department Management (Priority: P2) - Frontend

**Goal**: Implement department tree management page with CRUD and dropdown

**Independent Test**: View department tree, add/edit/delete departments, use department dropdown in forms

### Components & Views for US2

- [ ] T120 [P] [US2] Create frontend/src/components/common/TreeSelect.vue for tree dropdown selection
- [ ] T121 [P] [US2] Create frontend/src/api/department.ts with CRUD and tree methods
- [ ] T122 [US2] Create frontend/src/views/system/department/index.vue with tree table and CRUD dialog
- [ ] T123 [US2] Add department routes in frontend/src/router/routes.ts

**Checkpoint**: Department management UI complete

---

## Phase 12: User Story 3 - Position Management (Priority: P3) - Frontend

**Goal**: Implement position management page with status toggle and dropdown

**Independent Test**: View position list, add/edit/delete positions, toggle status, use position dropdown

### Views for US3

- [ ] T124 [P] [US3] Create frontend/src/api/position.ts with CRUD and options methods
- [ ] T125 [US3] Create frontend/src/views/system/position/index.vue with table and CRUD dialog
- [ ] T126 [US3] Add position routes in frontend/src/router/routes.ts

**Checkpoint**: Position management UI complete

---

## Phase 13: User Story 4 - Menu Management (Priority: P4) - Frontend

**Goal**: Implement menu tree management page with permission code editing

**Independent Test**: View menu tree, add/edit/delete menus with permission codes

### Views for US4

- [ ] T127 [P] [US4] Create frontend/src/api/menu.ts with CRUD and tree methods
- [ ] T128 [US4] Create frontend/src/views/system/menu/index.vue with tree table and CRUD dialog
- [ ] T129 [US4] Add menu routes in frontend/src/router/routes.ts

**Checkpoint**: Menu management UI complete

---

## Phase 14: User Story 5 - Role Management (Priority: P5) - Frontend

**Goal**: Implement role management page with permission tree assignment

**Independent Test**: View role list, add/edit roles, assign menu permissions via tree

### Components & Views for US5

- [ ] T130 [P] [US5] Create frontend/src/api/role.ts with CRUD and menu assignment methods
- [ ] T131 [US5] Create frontend/src/views/system/role/index.vue with table, CRUD dialog, and permission tree
- [ ] T132 [US5] Add role routes in frontend/src/router/routes.ts

**Checkpoint**: Role management UI complete

---

## Phase 15: User Story 6 - User Management (Priority: P6) - Frontend

**Goal**: Implement user management page with role assignment and avatar upload

**Independent Test**: View user list, add/edit users, reset password, upload avatar, toggle status

### Components & Views for US6

- [ ] T133 [P] [US6] Create frontend/src/components/upload/ImageUpload.vue for avatar upload
- [ ] T134 [P] [US6] Create frontend/src/components/common/PermissionButton.vue for permission-controlled buttons
- [ ] T135 [P] [US6] Update frontend/src/api/user.ts with CRUD, reset password, profile methods
- [ ] T136 [US6] Create frontend/src/views/system/user/index.vue with table, CRUD dialog, and filters
- [ ] T137 [US6] Create frontend/src/views/profile/index.vue for user profile editing
- [ ] T138 [US6] Add user and profile routes in frontend/src/router/routes.ts

**Checkpoint**: User management UI complete

---

## Phase 16: User Story 7 - Audit Logging (Priority: P7) - Frontend

**Goal**: Implement operation log and login log pages with filtering

**Independent Test**: View operation logs, filter by user/action/time, batch delete, view login logs

### Views for US7

- [ ] T139 [P] [US7] Create frontend/src/api/log.ts with operation and login log methods
- [ ] T140 [US7] Create frontend/src/views/log/operation/index.vue with table and filters
- [ ] T141 [US7] Create frontend/src/views/log/login/index.vue with table and filters
- [ ] T142 [US7] Add log routes in frontend/src/router/routes.ts

**Checkpoint**: All frontend UI complete - full system functional

---

## Phase 17: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

### Dynamic Routing & Permission Control

- [ ] T143 Implement dynamic route generation based on user permissions in frontend/src/router/index.ts
- [ ] T144 [P] Implement permission directive in frontend/src/utils/permission.ts for v-permission
- [ ] T145 Apply permission control to all buttons using PermissionButton component or v-permission directive

### Final Testing & Documentation

- [ ] T146 Run all backend tests with pytest and verify 100% pass
- [ ] T147 [P] Run all frontend tests with vitest and verify 100% pass
- [ ] T148 Run Black and Ruff on backend code and fix all issues
- [ ] T149 [P] Run ESLint and Prettier on frontend code and fix all issues
- [ ] T150 Verify docker-compose up starts all services correctly
- [ ] T151 Run quickstart.md validation - test all commands work
- [ ] T152 [P] Add OpenAPI descriptions and examples to all endpoints

### Performance & Security

- [ ] T153 Add database indexes per data-model.md specifications
- [ ] T154 [P] Implement Redis caching for user permissions
- [ ] T155 [P] Add rate limiting to login endpoint
- [ ] T156 Security review - verify no secrets in code, input validation on all endpoints

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **Backend US1-US7 (Phase 3-9)**: All depend on Foundational phase completion
  - US2-US7 depend on US1 (User model required)
  - US5-US6 depend on US4 (Menu model for permissions)
  - US6 depends on US2, US3, US5 (Department, Position, Role)
- **Frontend US1-US7 (Phase 10-16)**: All depend on corresponding Backend phases
  - Can start after Backend US1 is complete
- **Polish (Phase 17)**: Depends on all user stories being complete

### User Story Dependencies (Backend)

- **US1 (Auth)**: No dependencies - foundation for all others
- **US2 (Department)**: Depends on US1 (User model exists)
- **US3 (Position)**: Depends on US1 (User model exists)
- **US4 (Menu)**: Depends on US1 (User model exists)
- **US5 (Role)**: Depends on US4 (Menu model for permissions)
- **US6 (User)**: Depends on US2, US3, US5 (Department, Position, Role references)
- **US7 (Log)**: Depends on US1 (User model for logging)

### User Story Dependencies (Frontend)

- **US1 (Auth)**: Depends on Backend US1
- **US2-US7**: Can proceed in parallel after US1, depends on corresponding Backend phase

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before schemas
- Schemas before CRUD
- CRUD before routers
- Routers before registration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Within each user story, models/schemas marked [P] can run in parallel
- Frontend API files can be created in parallel with views
- Different user stories can be worked on in parallel after dependencies met

---

## Parallel Example: User Story 1 Backend

```bash
# Launch all tests for User Story 1 together:
Task: T043 [P] [US1] Create backend/tests/unit/test_security.py
Task: T044 [P] [US1] Create backend/tests/unit/test_captcha.py
Task: T045 [P] [US1] Create backend/tests/api/test_auth.py

# Launch all models/schemas for User Story 1 together:
Task: T046 [P] [US1] Create backend/app/models/user.py
Task: T047 [P] [US1] Create backend/app/models/login_log.py
Task: T048 [P] [US1] Create backend/app/schemas/auth.py
Task: T049 [P] [US1] Create backend/app/schemas/user.py
```

---

## Implementation Strategy

### MVP First (Backend US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 Backend
4. **STOP and VALIDATE**: Test login with Postman/curl
5. Deploy backend MVP if ready

### Incremental Delivery (Full System)

1. Complete Setup + Foundational → Foundation ready
2. Complete Backend US1 → Auth ready → Deploy
3. Complete Backend US2-US7 → All APIs ready → Deploy
4. Complete Frontend US1 → Login UI ready → Deploy
5. Complete Frontend US2-US7 → Full system ready → Deploy
6. Complete Polish → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: Backend US1 → US2 → US3
   - Developer B: Backend US4 → US5
   - Developer C: Backend US6 → US7
3. After Backend US1:
   - Developer D: Frontend US1 → US2
   - Developer E: Frontend US3 → US4
   - Developer F: Frontend US5 → US6 → US7
4. All stories integrate and work independently

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Tasks** | 156 |
| Setup Tasks | 16 |
| Foundational Tasks | 26 |
| Backend US1 (Auth) | 14 |
| Backend US2 (Dept) | 8 |
| Backend US3 (Pos) | 8 |
| Backend US4 (Menu) | 9 |
| Backend US5 (Role) | 11 |
| Backend US6 (User) | 9 |
| Backend US7 (Log) | 8 |
| Frontend US1 (Auth) | 9 |
| Frontend US2 (Dept) | 4 |
| Frontend US3 (Pos) | 3 |
| Frontend US4 (Menu) | 3 |
| Frontend US5 (Role) | 3 |
| Frontend US6 (User) | 6 |
| Frontend US7 (Log) | 4 |
| Polish Tasks | 14 |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend must be complete before frontend can fully function
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence