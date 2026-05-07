# 📋 TaskFlow — Team Task Manager

A full-stack web application for managing projects, assigning tasks, and tracking team progress with role-based access control (Admin/Member).

Built with **Python + FastAPI** backend and **Jinja2 + Vanilla JS** frontend. Deployable on Railway in minutes.

---

## 🚀 Features

- **Authentication** — Signup, Login, Logout with JWT (stored as HttpOnly cookie)
- **Project Management** — Create, update, delete projects; view all your projects on a dashboard
- **Team Management** — Add/remove members per project with Admin or Member roles
- **Task Management** — Create tasks with title, description, priority, due date, and assignee
- **Kanban Board** — Visual 3-column board (To Do / In Progress / Done) per project
- **Dashboard** — Stats overview: total, todo, in-progress, done, and overdue task counts
- **Role-Based Access Control** — Admins can do everything; Members can only update status of their own tasks
- **Overdue Detection** — Tasks past their due date are visually flagged in red
- **Railway Deployment** — Procfile + railway.toml included for one-click deploy

---

## 🗂️ Project Structure

```
Ethara/
├── main.py                  # FastAPI app, page routes, startup
├── config.py                # Environment settings (Pydantic)
├── database.py              # SQLAlchemy engine + session
├── models.py                # ORM models: User, Project, ProjectMember, Task
├── schemas.py               # Pydantic request/response schemas
├── auth.py                  # JWT creation/decoding, bcrypt hashing
├── dependencies.py          # FastAPI dependency injectors (auth, RBAC)
├── routers/
│   ├── __init__.py
│   ├── auth_router.py       # POST /api/auth/register|login|logout
│   ├── projects_router.py   # CRUD /api/projects/ + member management
│   ├── tasks_router.py      # CRUD /api/tasks/
│   └── users_router.py      # GET /api/users/me and /api/users/
├── templates/
│   ├── base.html            # Shared navbar layout
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Stats + project grid + recent tasks
│   └── project.html         # Kanban board + member management
├── static/
│   ├── style.css            # Full dark-theme stylesheet
│   └── app.js               # Modal helpers, logout, date utils
├── requirements.txt
├── Procfile                 # Railway: uvicorn start command
├── railway.toml             # Railway build + deploy config
└── .env.example             # Environment variable template
```

---

## ⚙️ Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3.11, FastAPI              |
| Database    | SQLite (dev) / PostgreSQL (prod)  |
| ORM         | SQLAlchemy 2.0                    |
| Auth        | JWT (python-jose) + bcrypt        |
| Templating  | Jinja2                            |
| Frontend    | Vanilla JS, CSS3                  |
| Server      | Uvicorn (ASGI)                    |
| Deployment  | Railway                           |

---

## 📦 Requirements

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

---

## 🛠️ Local Setup

### 1. Clone / download the project

```bash
cd Ethara
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> On Windows if you hit permission errors:
> ```bash
> pip install -r requirements.txt --user
> ```

### 3. Configure environment

```bash
copy .env.example .env
```

Edit `.env` if needed (the defaults work for local SQLite development).

### 4. Run the server

```bash
python -m uvicorn main:app --reload
```

### 5. Open in browser

```
http://127.0.0.1:8000
```

The SQLite database (`taskmanager.db`) is created automatically on first run — no manual setup required.

---

## 🌐 API Endpoints

### Auth
| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| POST   | `/api/auth/register`  | Create new account |
| POST   | `/api/auth/login`     | Login              |
| POST   | `/api/auth/logout`    | Logout             |

### Projects
| Method | Endpoint                               | Description              |
|--------|----------------------------------------|--------------------------|
| GET    | `/api/projects/`                       | List my projects         |
| POST   | `/api/projects/`                       | Create project           |
| GET    | `/api/projects/{id}`                   | Get project details      |
| PUT    | `/api/projects/{id}`                   | Update project (Admin)   |
| DELETE | `/api/projects/{id}`                   | Delete project (Owner)   |
| POST   | `/api/projects/{id}/members`           | Add member (Admin)       |
| DELETE | `/api/projects/{id}/members/{user_id}` | Remove member (Admin)    |

### Tasks
| Method | Endpoint          | Description                    |
|--------|-------------------|--------------------------------|
| GET    | `/api/tasks/`     | List tasks (filter by project) |
| POST   | `/api/tasks/`     | Create task                    |
| GET    | `/api/tasks/{id}` | Get task detail                |
| PUT    | `/api/tasks/{id}` | Update task                    |
| DELETE | `/api/tasks/{id}` | Delete task (Admin only)       |

### Users
| Method | Endpoint        | Description       |
|--------|-----------------|-------------------|
| GET    | `/api/users/me` | Current user info |
| GET    | `/api/users/`   | List all users    |

> Full interactive API docs available at `http://127.0.0.1:8000/docs`

---

## 🔐 Role-Based Access Control

| Action                    | Admin | Member |
|---------------------------|-------|--------|
| Create / delete project   | ✅    | ❌     |
| Add / remove members      | ✅    | ❌     |
| Create tasks              | ✅    | ✅     |
| Assign tasks to others    | ✅    | ✅     |
| Update own task status    | ✅    | ✅     |
| Update any task field     | ✅    | ❌     |
| Delete tasks              | ✅    | ❌     |
| View dashboard & board    | ✅    | ✅     |

---

## ☁️ Deploy to Railway

1. Push your code to a GitHub repository
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Select your repository
4. Add environment variables in Railway dashboard:
   ```
   SECRET_KEY=your-strong-random-key
   DATABASE_URL=postgresql://...   ← Railway provides this if you add a Postgres plugin
   ```
5. Railway auto-detects the `Procfile` and deploys

> For production, add a **PostgreSQL** plugin in Railway and set `DATABASE_URL` to the provided connection string.

---

## 📸 Pages

| Page       | Route              | Description                          |
|------------|--------------------|--------------------------------------|
| Login      | `/login`           | Email + password sign in             |
| Register   | `/register`        | Create a new account                 |
| Dashboard  | `/dashboard`       | Stats cards, project grid, task feed |
| Project    | `/projects/{id}`   | Kanban board, member management      |
| API Docs   | `/docs`            | Auto-generated Swagger UI            |

---

## 📝 Submission Checklist

- [x] Live URL (Railway deployment)
- [x] GitHub repository
- [x] README (this file)
- [ ] 2–5 min demo video

---

## 👤 Author

**Sai Varun**  
Built as part of the Team Task Manager Full-Stack Assignment.
