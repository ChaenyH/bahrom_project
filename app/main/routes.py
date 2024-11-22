from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Expense, db
from datetime import datetime
from . import main

project_templates = {
    1: {"template": "project_1_detail.html", "title": "윤리적 소비 가이드"},
    2: {"template": "project_2_detail.html", "title": "여행 계획 및 예산 관리"}
}

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/projects')
def projects():
    return render_template('projects.html')

@main.route('/projects/<int:project_id>')
def project_detail(project_id):
    project_info = project_templates.get(project_id)
    if not project_info:
        return render_template('404.html'), 404
    return render_template(project_info["template"], project={"id": project_id, "title": project_info["title"]})

@main.route('/budget', methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        date = request.form.get("date") or datetime.now().strftime('%Y-%m-%d')
        category = request.form.get("category")
        amount = float(request.form.get("amount"))
        memo = request.form.get("memo", "")
        expense = Expense(date=date, category=category, amount=amount, memo=memo)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("main.budget"))

    expenses = Expense.query.all()
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = 1000000 - total_spent  # 기본 예산 설정
    return render_template("budget.html", expenses=expenses, total_spent=total_spent, remaining_budget=remaining_budget)
