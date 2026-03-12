# Research: RBAC Admin System

**Feature**: 001-rbac-admin-system
**Date**: 2026-03-12

## Research Tasks

### 1. JWT Authentication Best Practices

**Decision**: Use PyJWT with RS256 or HS256 algorithm, access token + refresh token pattern

**Rationale**: 
- PyJWT is the standard Python JWT library, well-maintained and widely adopted
- Access token (2h) + refresh token (7d) provides balance between security and UX
- Store tokens in Redis for invalidation capability (logout, password change)
- Use HS256 for simplicity (single server), upgrade to RS256 if microservices needed

**Alternatives Considered**:
- python-jose: More features but heavier dependency
- authlib: Good for OAuth but overkill for simple JWT
- Session-based auth: Not suitable for SPA + API architecture

### 2. SQLAlchemy 2.0 Async Patterns

**Decision**: Use async session with async context manager pattern

**Rationale**:
```python
# Recommended pattern
async with async_session() as session:
    async with session.begin():
        # operations
```
- SQLAlchemy 2.0 native async support is production-ready
- Context managers ensure proper session cleanup
- Use `select()`, `insert()`, `update()`, `delete()` constructs (not legacy ORM queries)
- Eager loading with `selectinload()` for relationships

**Key Patterns**:
- Base model with `id`, `created_at`, `updated_at` fields
- Use `Mapped` type hints for all columns
- Async generators for large result sets

### 3. Redis Integration Patterns

**Decision**: Use redis-py (v5+) with async support

**Rationale**:
- redis-py is the de-facto Python Redis client
- v5+ has native async support via `redis.asyncio`
- Use for: captcha storage (5 min TTL), JWT blacklist, user permission cache

**Use Cases**:
| Key Pattern | Purpose | TTL |
|-------------|---------|-----|
| `captcha:{uuid}` | Store captcha code | 5 minutes |
| `token:blacklist:{jti}` | Invalidated tokens | Token expiry |
| `user:perms:{user_id}` | Cached permissions | 30 minutes |

### 4. Tree Structure Implementation

**Decision**: Use Adjacency List pattern with recursive CTE for queries

**Rationale**:
- Simple to implement: `parent_id` foreign key
- MySQL 8 supports recursive CTEs for tree traversal
- Balance between simplicity and performance
- Alternative: Nested Sets (complex updates), Materialized Path (good for reads)

**Implementation**:
```sql
-- Recursive CTE for department tree
WITH RECURSIVE dept_tree AS (
    SELECT * FROM departments WHERE id = :root_id
    UNION ALL
    SELECT d.* FROM departments d
    JOIN dept_tree t ON d.parent_id = t.id
)
SELECT * FROM dept_tree;
```

### 5. File Upload Strategy

**Decision**: Local filesystem with abstracted storage interface, optional OSS support

**Rationale**:
- Start simple with local storage
- Abstract storage interface allows future migration to cloud (Aliyun OSS, AWS S3)
- Use `python-multipart` for FastAPI file uploads
- Validate file type by content (not just extension), limit size

**Interface Design**:
```python
class StorageBackend(Protocol):
    async def save(self, file: UploadFile, path: str) -> str: ...
    async def delete(self, path: str) -> bool: ...
    async def get_url(self, path: str) -> str: ...
```

### 6. Permission Control Architecture

**Decision**: Permission codes stored in menus, roles aggregate permissions, users inherit from roles

**Rationale**:
- Menu items have permission codes (e.g., `user:create`, `user:delete`)
- Roles are assigned menus, creating permission sets
- Users have multiple roles, permissions are union of all role permissions
- Backend: middleware checks permission on each request
- Frontend: hide/show buttons based on cached permissions

**Permission Check Flow**:
1. User logs in → fetch user's roles → fetch all menu permissions
2. Cache permissions in Redis + Pinia store
3. Frontend: `v-if="hasPermission('user:create')"` for buttons
4. Backend: `@require_permission('user:create')` decorator on endpoints

### 7. Logging Strategy

**Decision**: Use loguru for application logging, automatic operation log capture

**Rationale**:
- loguru is simpler than standard logging, single-file setup
- Structured logging with JSON format for production
- Separate concerns: request logging (middleware), operation logging (decorator)

**Logging Layers**:
- Request/Response: Middleware logs all HTTP requests
- Operation: Decorator captures CRUD operations to database
- Error: Exception handler logs errors with stack trace

### 8. Frontend State Management

**Decision**: Pinia with composition API, separate stores for user, permission, app state

**Rationale**:
- Pinia is Vue 3 recommended state management (replaces Vuex)
- TypeScript support out of the box
- Modular stores for maintainability

**Store Structure**:
- `userStore`: Current user info, login/logout
- `permissionStore`: Routes, permissions, menu tree
- `appStore`: Sidebar state, tabs, theme

### 9. Dynamic Routing Pattern

**Decision**: Backend returns user's accessible menus, frontend generates routes dynamically

**Rationale**:
- More secure than static routes with guards
- Reduces frontend bundle size
- Routes are permission-controlled at database level

**Flow**:
1. Login success → request `/api/user/menus`
2. Backend returns menu tree filtered by user permissions
3. Frontend transforms menus to Vue Router routes
4. `router.addRoute()` for each route
5. Redirect to first accessible route

### 10. Database Migration Strategy

**Decision**: Alembic with auto-generation, manual review required

**Rationale**:
- Alembic is SQLAlchemy's official migration tool
- `alembic revision --autogenerate` creates migration from model changes
- Always review generated migrations before applying
- Use meaningful migration messages

**Workflow**:
```bash
alembic revision --autogenerate -m "add user table"
alembic upgrade head
```

## Technology Decisions Summary

| Component | Technology | Version | Reason |
|-----------|-----------|---------|--------|
| Backend Framework | FastAPI | 0.109+ | Async, auto OpenAPI, type hints |
| ORM | SQLAlchemy | 2.0+ | Native async, mature |
| Database | MySQL | 8.0+ | Recursive CTE, JSON support |
| Cache | Redis | 7.0+ | Session, captcha, permission cache |
| Auth | PyJWT | 2.8+ | Standard JWT implementation |
| Validation | Pydantic | 2.5+ | FastAPI native, strict mode |
| Migrations | Alembic | 1.13+ | SQLAlchemy standard |
| Logging | loguru | 0.7+ | Simple, structured |
| File Upload | python-multipart | 0.0.6+ | FastAPI file handling |
| Frontend Framework | Vue | 3.4+ | Composition API, TypeScript |
| Build Tool | Vite | 5.0+ | Fast HMR, ESM native |
| UI Library | Element Plus | 2.5+ | Comprehensive, Vue 3 native |
| State Management | Pinia | 2.1+ | Vue 3 recommended |
| HTTP Client | axios | 1.6+ | Interceptors, transformers |
| Router | Vue Router | 4.2+ | Vue 3 official |

## Performance Considerations

1. **Database Indexing**:
   - Index on `users.username`, `users.email`
   - Index on foreign keys: `department_id`, `position_id`, `role_id`
   - Composite index on `login_logs(user_id, created_at)`
   - Composite index on `operation_logs(user_id, created_at)`

2. **Query Optimization**:
   - Use `selectinload` for N+1 prevention
   - Pagination with `LIMIT/OFFSET` for small pages
   - Consider cursor pagination for large datasets

3. **Caching Strategy**:
   - Cache user permissions in Redis (30 min TTL)
   - Cache menu tree for each user
   - Invalidate on role/permission change

4. **Frontend Optimization**:
   - Route-level code splitting
   - Lazy load Element Plus components
   - Virtual scroll for large lists