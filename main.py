# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from config import settings
from database import get_db, create_tables
from models import Project, ProjectMember, Task, TaskStatus, User
from schemas import DashboardStats, ProjectOut, TaskOut
from dependencies import get_optional_user, get_current_user
from routers import auth_router, projects_router, tasks_router, users_router

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

# ─── Static & Templates ──────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ─── API Routers ─────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(tasks_router.router)
app.include_router(users_router.router)


# ─── Startup ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    create_tables()


# ─── Template / Page Routes ──────────────────────────────────────────────────

@app.get("/")
def index(request: Request, user: Optional[User] = Depends(get_optional_user)):
    if user:
        return RedirectResponse("/dashboard")
    return RedirectResponse("/login")


@app.get("/login")
def login_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
def register_page(request: Request, user: Optional[User] = Depends(get_optional_user)):
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Gather stats
    owned_ids = [p.id for p in db.query(Project).filter(Project.owner_id == current_user.id).all()]
    member_ids = [m.project_id for m in db.query(ProjectMember).filter(ProjectMember.user_id == current_user.id).all()]
    all_project_ids = list(set(owned_ids + member_ids))

    tasks = db.query(Task).filter(Task.project_id.in_(all_project_ids)).all()
    now = datetime.utcnow()

    stats = {
        "total": len(tasks),
        "todo": sum(1 for t in tasks if t.status == TaskStatus.todo),
        "in_progress": sum(1 for t in tasks if t.status == TaskStatus.in_progress),
        "done": sum(1 for t in tasks if t.status == TaskStatus.done),
        "overdue": sum(1 for t in tasks if t.due_date and t.due_date < now and t.status != TaskStatus.done),
    }

    projects = db.query(Project).filter(Project.id.in_(all_project_ids)).all()
    recent_tasks = (
        db.query(Task)
        .filter(Task.project_id.in_(all_project_ids))
        .order_by(Task.updated_at.desc())
        .limit(10)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "stats": stats,
            "projects": projects,
            "recent_tasks": recent_tasks,
            "now": now,
        },
    )


@app.get("/projects/{project_id}")
def project_page(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return RedirectResponse("/dashboard")

    # Check access
    is_owner = project.owner_id == current_user.id
    member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id)
        .first()
    )
    if not is_owner and not member:
        return RedirectResponse("/dashboard")

    is_admin = is_owner or (member and member.role.value == "admin")
    tasks = db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).all()
    members = (
        db.query(ProjectMember, User)
        .join(User, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )
    all_users = db.query(User).filter(User.is_active == True).all()  # noqa: E712
    now = datetime.utcnow()

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "user": current_user,
            "project": project,
            "tasks": tasks,
            "members": members,
            "all_users": all_users,
            "is_admin": is_admin,
            "now": now,
        },
    )
