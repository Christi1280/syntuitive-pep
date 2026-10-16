from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("")
def dashboard():
    return render_template("admin/dashboard.html", title="Admin Studio", active_page="Admin Studio")


@admin_bp.get("/lessons")
def lessons():
    return render_template("admin/lessons.html", title="Manage Lessons", active_page="Admin Studio")


@admin_bp.get("/questions")
def questions():
    return render_template("admin/questions.html", title="Question Bank", active_page="Admin Studio")


@admin_bp.get("/tests")
def tests():
    return render_template("admin/tests.html", title="Test Builder", active_page="Admin Studio")
