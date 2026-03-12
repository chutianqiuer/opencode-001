# Data Model: RBAC Admin System

**Feature**: 001-rbac-admin-system
**Date**: 2026-03-12

## Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────<│  UserRole   │>────│   Role      │
└─────────────┘     └─────────────┘     └─────────────┘
      │                                        │
      │                                        │
      ▼                                        ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Department  │     │  RoleMenu   │>────│    Menu     │
└─────────────┘     └─────────────┘     └─────────────┘
      │
      │
┌─────────────┐
│  Position   │
└─────────────┘

┌─────────────┐     ┌─────────────┐
│OperationLog │     │  LoginLog   │
└─────────────┘     └─────────────┘
```

## Entities

### User

**Description**: System user account with authentication credentials and profile information.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| password | VARCHAR(255) | NOT NULL | Hashed password (bcrypt) |
| name | VARCHAR(50) | NOT NULL | Display name |
| email | VARCHAR(100) | UNIQUE | Email address |
| phone | VARCHAR(20) | | Phone number |
| avatar | VARCHAR(255) | | Avatar image path |
| department_id | BIGINT | FK → departments.id, NULL | Associated department |
| position_id | BIGINT | FK → positions.id, NULL | Associated position |
| status | TINYINT | DEFAULT 1 | 0=disabled, 1=enabled |
| is_superuser | BOOLEAN | DEFAULT FALSE | Super admin flag |
| last_login_at | DATETIME | NULL | Last login timestamp |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | DATETIME | NOT NULL, ON UPDATE NOW() | Last update time |
| deleted_at | DATETIME | NULL | Soft delete timestamp |

**Relationships**:
- Belongs to one Department (optional)
- Belongs to one Position (optional)
- Has many Roles through UserRole
- Has many OperationLogs
- Has many LoginLogs

**Validation Rules**:
- Username: 3-50 chars, alphanumeric and underscore only
- Password: min 8 chars, at least 1 letter and 1 number
- Email: valid email format if provided
- Phone: optional, valid phone format

---

### Department

**Description**: Organizational unit in tree hierarchy.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| name | VARCHAR(50) | NOT NULL | Department name |
| code | VARCHAR(50) | UNIQUE, NOT NULL | Department code |
| parent_id | BIGINT | FK → departments.id, NULL | Parent department (NULL for root) |
| sort | INT | DEFAULT 0 | Sort order |
| leader | VARCHAR(50) | | Department leader name |
| phone | VARCHAR(20) | | Contact phone |
| email | VARCHAR(100) | | Contact email |
| status | TINYINT | DEFAULT 1 | 0=disabled, 1=enabled |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | DATETIME | NOT NULL, ON UPDATE NOW() | Last update time |
| deleted_at | DATETIME | NULL | Soft delete timestamp |

**Relationships**:
- Has one parent Department (self-referential)
- Has many child Departments
- Has many Users

**Validation Rules**:
- Name: required, 1-50 chars
- Code: required, unique, alphanumeric
- Tree depth: max 10 levels

---

### Position

**Description**: Job position within the organization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| name | VARCHAR(50) | NOT NULL | Position name |
| code | VARCHAR(50) | UNIQUE, NOT NULL | Position code |
| sort | INT | DEFAULT 0 | Sort order |
| status | TINYINT | DEFAULT 1 | 0=disabled, 1=enabled |
| remark | VARCHAR(255) | | Additional notes |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | DATETIME | NOT NULL, ON UPDATE NOW() | Last update time |
| deleted_at | DATETIME | NULL | Soft delete timestamp |

**Relationships**:
- Has many Users

**Validation Rules**:
- Name: required, 1-50 chars
- Code: required, unique, alphanumeric

---

### Menu

**Description**: Navigation menu item with permission code.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| name | VARCHAR(50) | NOT NULL | Menu name (display text) |
| code | VARCHAR(100) | UNIQUE, NOT NULL | Permission code |
| type | TINYINT | NOT NULL | 0=directory, 1=menu, 2=button |
| parent_id | BIGINT | FK → menus.id, NULL | Parent menu |
| path | VARCHAR(255) | | Frontend route path |
| component | VARCHAR(255) | | Vue component path |
| icon | VARCHAR(50) | | Menu icon name |
| sort | INT | DEFAULT 0 | Sort order |
| visible | TINYINT | DEFAULT 1 | 0=hidden, 1=visible |
| status | TINYINT | DEFAULT 1 | 0=disabled, 1=enabled |
| cache | TINYINT | DEFAULT 0 | 0=no cache, 1=keep-alive |
| remark | VARCHAR(255) | | Additional notes |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | DATETIME | NOT NULL, ON UPDATE NOW() | Last update time |
| deleted_at | DATETIME | NULL | Soft delete timestamp |

**Relationships**:
- Has one parent Menu (self-referential)
- Has many child Menus
- Has many Roles through RoleMenu

**Validation Rules**:
- Name: required, 1-50 chars
- Code: required, unique (e.g., `system:user:list`, `system:user:create`)
- Type: 0 (directory), 1 (menu/page), 2 (button)
- Path: required for type=1
- Component: required for type=1

---

### Role

**Description**: Role with assigned menu permissions.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| name | VARCHAR(50) | NOT NULL | Role name |
| code | VARCHAR(50) | UNIQUE, NOT NULL | Role code |
| sort | INT | DEFAULT 0 | Sort order |
| status | TINYINT | DEFAULT 1 | 0=disabled, 1=enabled |
| remark | VARCHAR(255) | | Additional notes |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |
| updated_at | DATETIME | NOT NULL, ON UPDATE NOW() | Last update time |
| deleted_at | DATETIME | NULL | Soft delete timestamp |

**Relationships**:
- Has many Users through UserRole
- Has many Menus through RoleMenu

**Validation Rules**:
- Name: required, 1-50 chars
- Code: required, unique, alphanumeric (e.g., `admin`, `editor`)

---

### UserRole (Junction Table)

**Description**: Many-to-many relationship between users and roles.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| user_id | BIGINT | FK → users.id, NOT NULL | User reference |
| role_id | BIGINT | FK → roles.id, NOT NULL | Role reference |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |

**Constraints**:
- UNIQUE(user_id, role_id)

---

### RoleMenu (Junction Table)

**Description**: Many-to-many relationship between roles and menus.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| role_id | BIGINT | FK → roles.id, NOT NULL | Role reference |
| menu_id | BIGINT | FK → menus.id, NOT NULL | Menu reference |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |

**Constraints**:
- UNIQUE(role_id, menu_id)

---

### OperationLog

**Description**: Audit record of user operations.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| user_id | BIGINT | FK → users.id, NULL | User who performed action |
| username | VARCHAR(50) | NOT NULL | Username (for deleted users) |
| module | VARCHAR(50) | NOT NULL | Module name (e.g., user, role) |
| action | VARCHAR(50) | NOT NULL | Action type (create, update, delete) |
| method | VARCHAR(10) | NOT NULL | HTTP method (GET, POST, PUT, DELETE) |
| url | VARCHAR(255) | NOT NULL | Request URL |
| params | TEXT | | Request parameters/body |
| ip | VARCHAR(50) | NOT NULL | Client IP address |
| user_agent | VARCHAR(255) | | Browser user agent |
| status | TINYINT | NOT NULL | 0=failure, 1=success |
| error_msg | TEXT | | Error message if failed |
| duration | INT | | Request duration in ms |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |

**Indexes**:
- INDEX(user_id, created_at)
- INDEX(module, action)
- INDEX(created_at)

---

### LoginLog

**Description**: Record of login attempts.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGINT | PK, AUTO_INCREMENT | Primary key |
| user_id | BIGINT | FK → users.id, NULL | User who logged in |
| username | VARCHAR(50) | NOT NULL | Username attempted |
| ip | VARCHAR(50) | NOT NULL | Client IP address |
| location | VARCHAR(100) | | Geographic location (from IP) |
| browser | VARCHAR(50) | | Browser name |
| os | VARCHAR(50) | | Operating system |
| status | TINYINT | NOT NULL | 0=failure, 1=success |
| message | VARCHAR(255) | | Login result message |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Record creation time |

**Indexes**:
- INDEX(user_id, created_at)
- INDEX(username)
- INDEX(created_at)

---

## Seed Data

### Default Super Admin User

```json
{
  "username": "admin",
  "password": "Admin@123",
  "name": "超级管理员",
  "is_superuser": true,
  "status": 1
}
```

### Default Roles

| Name | Code | Description |
|------|------|-------------|
| 超级管理员 | super_admin | Full system access |
| 管理员 | admin | Standard admin access |
| 普通用户 | user | Basic user access |

### Default Menus (Partial)

| Name | Code | Type | Path |
|------|------|------|------|
| 系统管理 | system | 0 | /system |
| 用户管理 | system:user | 1 | /system/user |
| 新增用户 | system:user:create | 2 | - |
| 编辑用户 | system:user:update | 2 | - |
| 删除用户 | system:user:delete | 2 | - |
| 角色管理 | system:role | 1 | /system/role |
| 菜单管理 | system:menu | 1 | /system/menu |
| 部门管理 | system:dept | 1 | /system/dept |
| 岗位管理 | system:position | 1 | /system/position |
| 日志管理 | log | 0 | /log |
| 操作日志 | log:operation | 1 | /log/operation |
| 登录日志 | log:login | 1 | /log/login |

## Database Constraints

### Foreign Key Constraints

- `users.department_id` → `departments.id` (ON DELETE SET NULL)
- `users.position_id` → `positions.id` (ON DELETE SET NULL)
- `departments.parent_id` → `departments.id` (ON DELETE CASCADE)
- `menus.parent_id` → `menus.id` (ON DELETE CASCADE)
- `user_roles.user_id` → `users.id` (ON DELETE CASCADE)
- `user_roles.role_id` → `roles.id` (ON DELETE CASCADE)
- `role_menus.role_id` → `roles.id` (ON DELETE CASCADE)
- `role_menus.menu_id` → `menus.id` (ON DELETE CASCADE)
- `operation_logs.user_id` → `users.id` (ON DELETE SET NULL)
- `login_logs.user_id` → `users.id` (ON DELETE SET NULL)