# API Contracts: RBAC Admin System

**Feature**: 001-rbac-admin-system
**Date**: 2026-03-12
**Base URL**: `/api/v1`

## Common Response Structure

All API responses follow this unified format:

```typescript
interface ApiResponse<T> {
  code: number;      // 200=success, 400=bad request, 401=unauthorized, 403=forbidden, 500=server error
  message: string;   // Human-readable message
  data: T | null;    // Response payload
}
```

## Pagination Request/Response

```typescript
interface PageRequest {
  page: number;      // Page number (1-indexed)
  page_size: number; // Items per page (default: 20)
  sort?: string;     // Sort field
  order?: 'asc' | 'desc'; // Sort order
}

interface PageResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

---

## Authentication Endpoints

### POST /auth/login

Login with username, password, and captcha.

**Request**:
```typescript
{
  username: string;    // Required, 3-50 chars
  password: string;    // Required, min 8 chars
  captcha_key: string; // Required, captcha UUID
  captcha_code: string; // Required, captcha code
}
```

**Response**:
```typescript
{
  code: 200;
  message: "登录成功";
  data: {
    access_token: string;  // JWT access token
    refresh_token: string; // JWT refresh token
    token_type: "bearer";
    expires_in: number;    // Access token expiry in seconds
  }
}
```

**Errors**:
- 400: Invalid credentials or captcha
- 401: Account disabled

---

### POST /auth/logout

Logout current user (invalidate tokens).

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "退出成功";
  data: null
}
```

---

### POST /auth/refresh

Refresh access token using refresh token.

**Request**:
```typescript
{
  refresh_token: string;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "刷新成功";
  data: {
    access_token: string;
    token_type: "bearer";
    expires_in: number;
  }
}
```

---

### GET /auth/captcha

Get captcha image for login.

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    captcha_key: string;    // UUID to verify captcha
    captcha_image: string;  // Base64 encoded image
  }
}
```

---

### GET /auth/user/info

Get current logged-in user info.

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    id: number;
    username: string;
    name: string;
    email: string;
    phone: string;
    avatar: string;
    department: {
      id: number;
      name: string;
    };
    position: {
      id: number;
      name: string;
    };
    roles: Array<{
      id: number;
      name: string;
      code: string;
    }>;
    permissions: string[]; // Array of permission codes
  }
}
```

---

## User Management Endpoints

### GET /users

Get paginated user list.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:list`

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `username`: Filter by username (optional)
- `name`: Filter by name (optional)
- `status`: Filter by status (optional)
- `department_id`: Filter by department (optional)

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    items: Array<{
      id: number;
      username: string;
      name: string;
      email: string;
      phone: string;
      avatar: string;
      department: { id: number; name: string } | null;
      position: { id: number; name: string } | null;
      roles: Array<{ id: number; name: string; code: string }>;
      status: number;
      last_login_at: string;
      created_at: string;
    }>;
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
}
```

---

### GET /users/{id}

Get user by ID.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:list`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    id: number;
    username: string;
    name: string;
    email: string;
    phone: string;
    avatar: string;
    department_id: number | null;
    position_id: number | null;
    role_ids: number[];
    status: number;
    created_at: string;
    updated_at: string;
  }
}
```

---

### POST /users

Create new user.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:create`

**Request**:
```typescript
{
  username: string;      // Required, unique, 3-50 chars
  password: string;      // Required, min 8 chars
  name: string;          // Required, 1-50 chars
  email?: string;        // Optional, valid email format
  phone?: string;        // Optional
  department_id?: number;
  position_id?: number;
  role_ids: number[];    // Required, at least one role
  status: number;        // Default: 1
}
```

**Response**:
```typescript
{
  code: 200;
  message: "创建成功";
  data: { id: number }
}
```

---

### PUT /users/{id}

Update user.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:update`

**Request**:
```typescript
{
  name?: string;
  email?: string;
  phone?: string;
  department_id?: number;
  position_id?: number;
  role_ids?: number[];
  status?: number;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### DELETE /users/{id}

Delete user.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:delete`

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

---

### PUT /users/{id}/status

Toggle user status.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:update`

**Request**:
```typescript
{
  status: number; // 0=disabled, 1=enabled
}
```

**Response**:
```typescript
{
  code: 200;
  message: "状态更新成功";
  data: null
}
```

---

### PUT /users/{id}/reset-password

Reset user password.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:user:update`

**Response**:
```typescript
{
  code: 200;
  message: "密码重置成功";
  data: {
    temp_password: string; // New temporary password
  }
}
```

---

### PUT /users/profile

Update current user profile.

**Headers**: `Authorization: Bearer {token}`

**Request**:
```typescript
{
  name?: string;
  email?: string;
  phone?: string;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### PUT /users/avatar

Upload avatar.

**Headers**: `Authorization: Bearer {token}`
**Content-Type**: `multipart/form-data`

**Request**: Form data with `file` field (image file, max 5MB)

**Response**:
```typescript
{
  code: 200;
  message: "上传成功";
  data: {
    avatar: string; // Avatar URL/path
  }
}
```

---

## Department Management Endpoints

### GET /departments

Get department tree.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:dept:list`

**Query Parameters**:
- `status`: Filter by status (optional)

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    code: string;
    parent_id: number | null;
    sort: number;
    leader: string;
    phone: string;
    email: string;
    status: number;
    children: this[]; // Recursive children
  }>
}
```

---

### GET /departments/tree

Get department tree for dropdown selection (simplified).

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    parent_id: number | null;
    children: this[];
  }>
}
```

---

### POST /departments

Create department.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:dept:create`

**Request**:
```typescript
{
  name: string;       // Required
  code: string;       // Required, unique
  parent_id?: number;
  sort?: number;
  leader?: string;
  phone?: string;
  email?: string;
  status?: number;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "创建成功";
  data: { id: number }
}
```

---

### PUT /departments/{id}

Update department.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:dept:update`

**Request**: Same as POST

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### DELETE /departments/{id}

Delete department.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:dept:delete`

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

**Errors**:
- 400: Department has children or users

---

## Position Management Endpoints

### GET /positions

Get paginated position list.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:position:list`

**Query Parameters**:
- `page`, `page_size`: Pagination
- `name`: Filter by name
- `status`: Filter by status

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    items: Array<{
      id: number;
      name: string;
      code: string;
      sort: number;
      status: number;
      remark: string;
      created_at: string;
    }>;
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
}
```

---

### GET /positions/options

Get active positions for dropdown.

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    code: string;
  }>
}
```

---

### POST /positions

Create position.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:position:create`

**Request**:
```typescript
{
  name: string;     // Required
  code: string;     // Required, unique
  sort?: number;
  status?: number;
  remark?: string;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "创建成功";
  data: { id: number }
}
```

---

### PUT /positions/{id}

Update position.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:position:update`

**Request**: Same as POST

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### DELETE /positions/{id}

Delete position.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:position:delete`

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

---

### PUT /positions/{id}/status

Toggle position status.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:position:update`

**Request**:
```typescript
{
  status: number;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "状态更新成功";
  data: null
}
```

---

## Menu Management Endpoints

### GET /menus

Get menu tree.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:menu:list`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    code: string;
    type: number;      // 0=directory, 1=menu, 2=button
    parent_id: number | null;
    path: string;
    component: string;
    icon: string;
    sort: number;
    visible: number;
    status: number;
    children: this[];
  }>
}
```

---

### GET /menus/tree

Get menu tree for role permission assignment.

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    code: string;
    type: number;
    parent_id: number | null;
    children: this[];
  }>
}
```

---

### POST /menus

Create menu.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:menu:create`

**Request**:
```typescript
{
  name: string;       // Required
  code: string;       // Required, unique
  type: number;       // Required, 0/1/2
  parent_id?: number;
  path?: string;      // Required if type=1
  component?: string; // Required if type=1
  icon?: string;
  sort?: number;
  visible?: number;
  status?: number;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "创建成功";
  data: { id: number }
}
```

---

### PUT /menus/{id}

Update menu.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:menu:update`

**Request**: Same as POST

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### DELETE /menus/{id}

Delete menu.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:menu:delete`

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

---

## Role Management Endpoints

### GET /roles

Get paginated role list.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:list`

**Query Parameters**:
- `page`, `page_size`: Pagination
- `name`: Filter by name
- `status`: Filter by status

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    items: Array<{
      id: number;
      name: string;
      code: string;
      sort: number;
      status: number;
      remark: string;
      created_at: string;
    }>;
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
}
```

---

### GET /roles/options

Get active roles for dropdown.

**Headers**: `Authorization: Bearer {token}`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: Array<{
    id: number;
    name: string;
    code: string;
  }>
}
```

---

### GET /roles/{id}

Get role by ID with assigned menu IDs.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:list`

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    id: number;
    name: string;
    code: string;
    sort: number;
    status: number;
    remark: string;
    menu_ids: number[]; // Assigned menu IDs
    created_at: string;
  }
}
```

---

### POST /roles

Create role.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:create`

**Request**:
```typescript
{
  name: string;       // Required
  code: string;       // Required, unique
  sort?: number;
  status?: number;
  remark?: string;
  menu_ids: number[]; // Required, at least one
}
```

**Response**:
```typescript
{
  code: 200;
  message: "创建成功";
  data: { id: number }
}
```

---

### PUT /roles/{id}

Update role.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:update`

**Request**: Same as POST

**Response**:
```typescript
{
  code: 200;
  message: "更新成功";
  data: null
}
```

---

### DELETE /roles/{id}

Delete role.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:delete`

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

**Errors**:
- 400: Role is assigned to users

---

### PUT /roles/{id}/status

Toggle role status.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `system:role:update`

**Request**:
```typescript
{
  status: number;
}
```

**Response**:
```typescript
{
  code: 200;
  message: "状态更新成功";
  data: null
}
```

---

## Audit Log Endpoints

### GET /logs/operation

Get paginated operation log list.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:operation:list`

**Query Parameters**:
- `page`, `page_size`: Pagination
- `user_id`: Filter by user
- `username`: Filter by username
- `module`: Filter by module
- `action`: Filter by action
- `status`: Filter by status
- `start_time`, `end_time`: Filter by time range

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    items: Array<{
      id: number;
      user_id: number;
      username: string;
      module: string;
      action: string;
      method: string;
      url: string;
      params: string;
      ip: string;
      status: number;
      error_msg: string;
      duration: number;
      created_at: string;
    }>;
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
}
```

---

### DELETE /logs/operation

Batch delete operation logs.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:operation:delete`

**Request**:
```typescript
{
  ids: number[];
}
```

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

---

### DELETE /logs/operation/clear

Clear all operation logs.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:operation:delete`

**Response**:
```typescript
{
  code: 200;
  message: "清空成功";
  data: null
}
```

---

### GET /logs/login

Get paginated login log list.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:login:list`

**Query Parameters**:
- `page`, `page_size`: Pagination
- `user_id`: Filter by user
- `username`: Filter by username
- `status`: Filter by status
- `start_time`, `end_time`: Filter by time range

**Response**:
```typescript
{
  code: 200;
  message: "success";
  data: {
    items: Array<{
      id: number;
      user_id: number;
      username: string;
      ip: string;
      location: string;
      browser: string;
      os: string;
      status: number;
      message: string;
      created_at: string;
    }>;
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
  }
}
```

---

### DELETE /logs/login

Batch delete login logs.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:login:delete`

**Request**:
```typescript
{
  ids: number[];
}
```

**Response**:
```typescript
{
  code: 200;
  message: "删除成功";
  data: null
}
```

---

### DELETE /logs/login/clear

Clear all login logs.

**Headers**: `Authorization: Bearer {token}`
**Permission**: `log:login:delete`

**Response**:
```typescript
{
  code: 200;
  message: "清空成功";
  data: null
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not found |
| 409 | Conflict (duplicate resource) |
| 500 | Internal server error |

## Rate Limiting

- Login endpoint: 5 requests per minute per IP
- API endpoints: 100 requests per minute per user