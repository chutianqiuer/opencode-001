# Feature Specification: RBAC Admin System

**Feature Branch**: `001-rbac-admin-system`
**Created**: 2026-03-12
**Status**: Draft
**Input**: User description: "构建一个企业级 FastAPI + Vue 通用后台管理系统（RBAC权限管理）"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication (Priority: P1)

As a system user, I need to securely log in to access the admin system with my assigned permissions, so that I can perform my authorized tasks.

**Why this priority**: Authentication is the foundation of the entire system. Without secure login, no other features can be safely accessed. All subsequent features depend on user identity verification.

**Independent Test**: Can be fully tested by accessing the login page, entering valid credentials, receiving a JWT token, and verifying protected endpoints require authentication. Delivers secure access control foundation.

**Acceptance Scenarios**:

1. **Given** I am an unauthenticated user on the login page, **When** I enter valid username and password with correct captcha, **Then** I receive a JWT token and am redirected to the dashboard
2. **Given** I am an unauthenticated user, **When** I enter invalid credentials or wrong captcha, **Then** I see an error message and remain on the login page
3. **Given** I am an authenticated user, **When** my JWT token expires, **Then** I am prompted to re-authenticate
4. **Given** I am an authenticated user, **When** I click logout, **Then** my session is invalidated and I am redirected to login page

---

### User Story 2 - Department Management (Priority: P2)

As an administrator, I need to manage the organizational department structure in a tree hierarchy, so that I can reflect the real organizational structure and assign users to appropriate departments.

**Why this priority**: Department structure is a prerequisite for user assignment and role scoping. Organizations need this before managing users.

**Independent Test**: Can be fully tested by creating, editing, and deleting department nodes in a tree structure, and verifying the dropdown list for department selection works correctly. Delivers organizational structure management.

**Acceptance Scenarios**:

1. **Given** I am an administrator, **When** I access the department management page, **Then** I see all departments in a tree structure with expand/collapse functionality
2. **Given** I am viewing the department tree, **When** I click "Add Department", **Then** I can create a new department under a selected parent or as root
3. **Given** I select a department, **When** I click "Edit", **Then** I can modify department name, code, and other attributes
4. **Given** I select a department with no child departments or users, **When** I click "Delete", **Then** the department is removed from the tree
5. **Given** I am on the user creation/edit form, **When** I click the department dropdown, **Then** I see all departments in a searchable tree format

---

### User Story 3 - Position Management (Priority: P3)

As an administrator, I need to manage job positions within the organization, so that I can assign appropriate roles and responsibilities to users.

**Why this priority**: Positions complement department structure and are needed before user assignment. Less critical than departments but still foundational.

**Independent Test**: Can be fully tested by performing CRUD operations on positions, toggling status, and verifying the dropdown list for position selection. Delivers job position management.

**Acceptance Scenarios**:

1. **Given** I am an administrator, **When** I access position management, **Then** I see a paginated list of all positions with name, code, status, and actions
2. **Given** I am on position management page, **When** I click "Add Position", **Then** I can create a new position with name, code, and status
3. **Given** I select a position, **When** I click "Edit", **Then** I can modify position details
4. **Given** I select an active position, **When** I toggle its status, **Then** the position becomes inactive and unavailable for assignment
5. **Given** I am on the user creation/edit form, **When** I click the position dropdown, **Then** I see only active positions in a searchable list

---

### User Story 4 - Menu & Permission Management (Priority: P4)

As a super administrator, I need to manage system menus and their associated permissions, so that I can control what features and buttons users can access.

**Why this priority**: Menu and permission definitions are required before role assignment. Super admin functionality needed for RBAC.

**Independent Test**: Can be fully tested by creating menu hierarchies, assigning permissions, and verifying menu items appear correctly based on permissions. Delivers permission infrastructure.

**Acceptance Scenarios**:

1. **Given** I am a super administrator, **When** I access menu management, **Then** I see all menus in a tree structure with icons, paths, and permission codes
2. **Given** I am on menu management, **When** I click "Add Menu", **Then** I can create a new menu item with name, path, icon, permission code, and parent menu
3. **Given** I select a menu item, **When** I click "Edit", **Then** I can modify all menu properties including permission codes
4. **Given** I select a menu with no children, **When** I click "Delete", **Then** the menu is removed
5. **Given** I define a menu with permission code "user:create", **When** this is assigned to a role, **Then** users with that role see the corresponding button

---

### User Story 5 - Role Management (Priority: P5)

As a super administrator, I need to manage roles and assign menu permissions to roles, so that users can be granted appropriate access levels.

**Why this priority**: Roles connect permissions to users. Requires menu/permission definitions to exist first.

**Independent Test**: Can be fully tested by creating roles, assigning menu permissions, and verifying users with those roles see appropriate menus and have correct button-level permissions. Delivers role-based access control.

**Acceptance Scenarios**:

1. **Given** I am a super administrator, **When** I access role management, **Then** I see a paginated list of all roles with name, code, status, and actions
2. **Given** I am on role management, **When** I click "Add Role", **Then** I can create a new role with name, code, status, and menu permission selection
3. **Given** I select a role, **When** I click "Edit", **Then** I can modify role details and assigned menu permissions via a permission tree
4. **Given** I select an active role, **When** I toggle its status, **Then** the role becomes inactive and users with this role lose access
5. **Given** I am assigning permissions to a role, **When** I select a menu item, **Then** I can also select specific button permissions within that menu

---

### User Story 6 - User Management (Priority: P6)

As an administrator, I need to manage user accounts including profile updates and password resets, so that users can access the system with appropriate permissions.

**Why this priority**: Users need roles and departments to exist first. Combines all previous elements.

**Independent Test**: Can be fully tested by creating users, assigning roles and departments, resetting passwords, and updating profiles including avatar upload. Delivers complete user account management.

**Acceptance Scenarios**:

1. **Given** I am an administrator, **When** I access user management, **Then** I see a paginated list of all users with username, name, department, role, and status
2. **Given** I am on user management, **When** I click "Add User", **Then** I can create a new user with username, name, department, position, role, and initial password
3. **Given** I select a user, **When** I click "Edit", **Then** I can modify user details except password
4. **Given** I select a user, **When** I click "Reset Password", **Then** the user receives a new temporary password
5. **Given** I select an active user, **When** I toggle status, **Then** the user is disabled and cannot log in
6. **Given** I am a logged-in user, **When** I access my profile, **Then** I can update my name, phone, email, and avatar
7. **Given** I am updating my profile, **When** I upload a new avatar image, **Then** the image is stored and displayed in the interface

---

### User Story 7 - Audit Logging (Priority: P7)

As a system auditor, I need to view operation logs and login logs, so that I can track user activities for security and compliance purposes.

**Why this priority**: Logging is essential for security audit but doesn't block other features. Can be added after core functionality.

**Independent Test**: Can be fully tested by performing various operations, then viewing operation logs and login logs with filtering and batch deletion. Delivers complete audit trail.

**Acceptance Scenarios**:

1. **Given** I am an administrator, **When** I access operation logs, **Then** I see a paginated list of all operations with user, action, time, IP, and details
2. **Given** I am viewing operation logs, **When** I filter by user, action type, or time range, **Then** I see only matching records
3. **Given** I select multiple operation logs, **When** I click "Delete", **Then** those records are removed
4. **Given** I am on operation logs page, **When** I click "Clear All", **Then** all logs are deleted after confirmation
5. **Given** I am an administrator, **When** I access login logs, **Then** I see a paginated list of all login attempts with user, time, IP, and status (success/failure)
6. **Given** I am viewing login logs, **When** I filter by user or time range, **Then** I see only matching records
7. **Given** Any user performs any create/update/delete action, **When** the action completes, **Then** an operation log entry is automatically created

---

### Edge Cases

- What happens when a user tries to delete a department that has child departments? System should prevent deletion and show warning message
- What happens when a user tries to delete a department that has users assigned? System should prevent deletion and show which users are affected
- What happens when a user tries to delete a role that is assigned to users? System should prevent deletion or offer to remove role from users first
- What happens when a user tries to delete a menu that is assigned to active roles? System should warn about impact or prevent deletion
- What happens when a user's JWT token is about to expire? System should offer token refresh or prompt re-login
- What happens when captcha fails multiple times? Account should be temporarily locked after threshold
- What happens when uploading an image that exceeds size limit or invalid format? System should reject with clear error message
- What happens when a user is assigned multiple roles with conflicting permissions? System should apply most permissive permission (union of all permissions)
- What happens when a user tries to access a page they don't have permission for? System should show 403 error or redirect to appropriate page
- What happens when concurrent edits occur on the same record? System should handle with optimistic locking or last-write-wins with notification

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Authorization

- **FR-001**: System MUST provide user login with username, password, and graphical captcha verification
- **FR-002**: System MUST generate JWT tokens upon successful authentication with configurable expiration
- **FR-003**: System MUST validate JWT tokens on all protected endpoints
- **FR-004**: System MUST support JWT token refresh for active sessions
- **FR-005**: System MUST implement permission-based access control for all menu items and buttons
- **FR-006**: System MUST enforce both frontend route guards and backend API authorization

#### Department Management

- **FR-007**: System MUST support tree-structured department hierarchy with unlimited depth
- **FR-008**: System MUST provide department CRUD operations (create, read, update, delete)
- **FR-009**: System MUST prevent deletion of departments with child departments
- **FR-010**: System MUST prevent deletion of departments with assigned users
- **FR-011**: System MUST provide department dropdown selection in tree format for forms

#### Position Management

- **FR-012**: System MUST provide position CRUD operations with name, code, and status fields
- **FR-013**: System MUST support position status toggle (active/inactive)
- **FR-014**: System MUST provide position dropdown list for user assignment (showing only active positions)

#### Menu & Permission Management

- **FR-015**: System MUST support tree-structured menu hierarchy with parent-child relationships
- **FR-016**: System MUST allow menus to have associated permission codes for button-level control
- **FR-017**: System MUST provide menu CRUD operations with path, icon, permission code, and sort order
- **FR-018**: System MUST support both page-level and button-level permission definitions

#### Role Management

- **FR-019**: System MUST provide role CRUD operations with name, code, and status fields
- **FR-020**: System MUST allow assigning multiple menu permissions to a role via permission tree selection
- **FR-021**: System MUST support role status toggle (active/inactive)
- **FR-022**: System MUST support assigning multiple roles to a single user

#### User Management

- **FR-023**: System MUST provide user CRUD operations with username, name, department, position, role, and status
- **FR-024**: System MUST support user status toggle (active/inactive)
- **FR-025**: System MUST allow administrators to reset user passwords with temporary password generation
- **FR-026**: System MUST allow users to update their own profile (name, phone, email)
- **FR-027**: System MUST support avatar image upload with size and format validation
- **FR-028**: System MUST enforce unique username constraint

#### Audit Logging

- **FR-029**: System MUST automatically record all create, update, delete operations with user, action, target, IP, and timestamp
- **FR-030**: System MUST record all login attempts (success and failure) with user, IP, and timestamp
- **FR-031**: System MUST provide paginated, filterable operation log listing
- **FR-032**: System MUST provide paginated, filterable login log listing
- **FR-033**: System MUST support batch deletion of log records
- **FR-034**: System MUST support clearing all log records with confirmation

#### Common Features

- **FR-035**: System MUST return all API responses in unified format `{code, message, data}`
- **FR-036**: System MUST implement CORS for cross-origin requests
- **FR-037**: System MUST provide logging middleware for request/response tracking
- **FR-038**: System MUST support file upload for images with configurable storage
- **FR-039**: System MUST use Redis for session management and caching
- **FR-040**: System MUST provide database initialization with seed data (default super admin, default roles)

### Key Entities

- **User**: Represents a system user with authentication credentials, assigned department, position, roles, and profile information including avatar
- **Department**: Represents organizational unit in tree hierarchy with name, code, parent reference, and sort order
- **Position**: Represents job position with name, code, status, and sort order
- **Menu**: Represents navigation menu item with name, path, icon, permission code, parent reference, and sort order
- **Role**: Represents a set of permissions with name, code, status, and assigned menu permissions
- **UserRole**: Junction entity representing the many-to-many relationship between users and roles
- **RoleMenu**: Junction entity representing the many-to-many relationship between roles and menus
- **OperationLog**: Represents audit record of user operations with user, action, target, IP, timestamp, and details
- **LoginLog**: Represents record of login attempts with user, IP, timestamp, status, and browser/OS information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete login in under 10 seconds including captcha verification
- **SC-002**: System supports at least 100 concurrent users without performance degradation
- **SC-003**: All API responses return within 500ms for normal operations (excluding file uploads)
- **SC-004**: 95% of users can navigate to their permitted features within 3 clicks from login
- **SC-005**: Permission changes take effect within 5 seconds for active users (via token refresh or cache invalidation)
- **SC-006**: All database queries complete within 200ms with proper indexing
- **SC-007**: File upload for avatars completes within 10 seconds for files under 5MB
- **SC-008**: System can be deployed and started with a single `docker-compose up` command
- **SC-009**: All CRUD operations provide user-friendly error messages for validation failures
- **SC-010**: Audit logs capture 100% of data modification operations with accurate timestamps

### Assumptions

- Default super administrator account will be created during initial setup
- Image files will be stored in local filesystem by default (configurable for cloud storage)
- Session timeout is configurable but defaults to 30 minutes of inactivity
- JWT token expiration defaults to 2 hours with refresh token of 7 days
- Password complexity requirements: minimum 8 characters, at least one letter and one number
- Supported image formats for upload: JPG, PNG, GIF with maximum size of 5MB
- Pagination defaults to 20 items per page with configurable limits
- Department tree depth is limited to 10 levels for performance
- Role name must be unique within the system
- Username must be unique within the system