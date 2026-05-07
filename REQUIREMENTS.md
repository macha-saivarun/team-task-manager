# Team Task Manager - Requirements & File Structure

## Tech Stack
- **Backend**: Python (FastAPI)
- **Database**: SQLite via SQLAlchemy (easily swappable to PostgreSQL)
- **Auth**: JWT (python-jose) + bcrypt password hashing
- **Frontend**: Jinja2 templates + vanilla JS (served by FastAPI)
- **Deployment**: Railway-ready (Procfile + railway.toml included)

## Python Package Requirements (requirements.txt)
```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
jinja2==3.1.4
aiofiles==23.2.1
pydantic==2.7.1
pydantic-settings==2.2.1
python-dotenv==1.0.1
```

## File Structure
```
team_task_manager/
├── main.py                  # FastAPI app entry point
├── config.py                # Settings / env vars
├── database.py              # DB engine + session
├── models.py                # SQLAlchemy ORM models
├── schemas.py               # Pydantic request/response schemas
├── auth.py                  # JWT + password utilities
├── dependencies.py          # FastAPI dependency injectors
├── routers/
│   ├── __init__.py
│   ├── auth_router.py       # /api/auth/*
│   ├── projects_router.py   # /api/projects/*
│   ├── tasks_router.py      # /api/tasks/*
│   └── users_router.py      # /api/users/*
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── project.html
│   └── task_detail.html
├── static/
│   ├── style.css
│   └── app.js
├── requirements.txt
├── Procfile                 # Railway deployment
├── railway.toml
└── .env.example
```

## Role-Based Access Control
| Action                        | Admin | Member |
|-------------------------------|-------|--------|
| Create / delete project       | ✅    | ❌     |
| Add / remove team members     | ✅    | ❌     |
| Create / assign tasks         | ✅    | ✅     |
| Update own task status        | ✅    | ✅     |
| Delete any task               | ✅    | ❌     |
| View dashboard                | ✅    | ✅     |

## API Endpoints
### Auth
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout

### Projects
- GET    /api/projects/
- POST   /api/projects/
- GET    /api/projects/{id}
- PUT    /api/projects/{id}
- DELETE /api/projects/{id}
- POST   /api/projects/{id}/members
- DELETE /api/projects/{id}/members/{user_id}

### Tasks
- GET    /api/tasks/?project_id=
- POST   /api/tasks/
- GET    /api/tasks/{id}
- PUT    /api/tasks/{id}
- DELETE /api/tasks/{id}

### Users
- GET    /api/users/me
- GET    /api/users/
