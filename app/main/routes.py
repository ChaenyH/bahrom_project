from flask import Blueprint, render_template, request, redirect, url_for
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

@main.route('/checklist-guide')
def checklist_guide():
    return render_template('checklist_guide.html')

@main.route('/ethical-consumption')
def ethical_consumption():
    return render_template('ethical_consumption.html')


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

# HTML: 사용자 등록
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="User already exists")

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))
    return render_template('register.html')

# HTML: 사용자 로그인
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error="Invalid email or password")
    return render_template('login.html')
