
import os

from urllib.request import urlopen
from urllib.error import URLError
from sqlalchemy import text

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from app import db
from app.models import Project, Task

main = Blueprint("main", __name__)


@main.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "TaskFlow",
        "instance": os.getenv("TASKFLOW_INSTANCE", "unknown")
    }), 200


@main.route("/")
def index():
    projects = Project.query.all()
    tasks = Project.query.all()

    recent_tasks = Task.query.order_by(
        Task.created_at.desc()
    ).limit(5).all()

    total_projects = Project.query.count()
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status="Готова").count()
    in_progress = Task.query.filter_by(status="В процес").count()

    return render_template(
        "index.html",
        projects=projects,
        tasks=recent_tasks,
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        in_progress=in_progress
    )


@main.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Името на проекта е задължително.", "error")
        else:
            project = Project(name=name, description=description)
            db.session.add(project)
            db.session.commit()
            flash("Проектът е добавен успешно!", "success")
            return redirect(url_for("main.projects"))

    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)


@main.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    project = db.get_or_404(Project, project_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            flash("Името е задължително.", "error")
        else:
            project.name = name
            project.description = request.form.get("description", "").strip()
            db.session.commit()
            flash("Проектът е редактиран!", "success")
            return redirect(url_for("main.projects"))

    return render_template("edit_project.html", project=project)


@main.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    project = db.get_or_404(Project, project_id)
    db.session.delete(project)
    db.session.commit()

    flash("Проектът е изтрит!", "success")
    return redirect(url_for("main.projects"))


@main.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        project_id = request.form.get("project_id", type=int)
        project = db.session.get(Project, project_id)

        if not title or project is None:
            flash("Въведи заглавие и избери проект.", "error")
        else:
            task = Task(
                title=title,
                description=request.form.get("description", "").strip(),
                status=request.form.get("status", "Предстои"),
                project=project
            )

            db.session.add(task)
            db.session.commit()
            flash("Задачата е добавена!", "success")
            return redirect(url_for("main.tasks"))

    all_tasks = Task.query.all()
    all_projects = Project.query.all()

    return render_template(
        "tasks.html",
        tasks=all_tasks,
        projects=all_projects
    )


@main.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        project_id = request.form.get("project_id", type=int)
        project = db.session.get(Project, project_id)

        if not title or project is None:
            flash("Въведи заглавие и избери проект.", "error")
        else:
            task.title = title
            task.description = request.form.get("description", "").strip()
            task.status = request.form.get("status", "Предстои")
            task.project = project

            db.session.commit()
            flash("Задачата е редактирана!", "success")
            return redirect(url_for("main.tasks"))

    projects_list = Project.query.all()

    return render_template(
        "edit_task.html",
        task=task,
        projects=projects_list
    )


@main.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    flash("Задачата е изтрита!", "success")
    return redirect(url_for("main.tasks"))



def check_service(url):
    try:
        with urlopen(url, timeout=3) as response:
            return response.status == 200
    except (URLError, TimeoutError, OSError):
        return False


@main.route("/monitoring")
def monitoring():
    nginx_ok = check_service("http://nginx/health")
    web1_ok = check_service("http://web1:5000/health")
    web2_ok = check_service("http://web2:5000/health")

    try:
        db.session.execute(text("SELECT 1"))
        database_ok = True
    except Exception:
        db.session.rollback()
        database_ok = False

    statuses = {
        "Nginx Load Balancer": nginx_ok,
        "Flask Web 1": web1_ok,
        "Flask Web 2": web2_ok,
        "PostgreSQL": database_ok
    }

    return render_template(
        "monitoring.html",
        statuses=statuses
    )

