from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from app.main.models import db, User, Travel
from datetime import datetime
from . import main

def get_user_data(user_id):
    # 데이터베이스에서 사용자 데이터 가져오기
    user = User.query.get(user_id)
    if not user:
        return None  # 사용자가 없으면 None 반환
    return {
        "username": user.username,
        "email": user.email,
        "travels": user.travels  # 여행 데이터가 있다면 포함
    }

@main.route('/')
def home():
    return render_template('index.html')

# HTML: 사용자 등록
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        print(f"Received data: username={username}, email={email}, password={password}")

        # 입력값 유효성 검사
        if not email or not password or not username:
            return render_template('signup.html', error="모든 필드를 입력해주세요")
        if password != confirm_password:
            return render_template('signup.html', error="비밀번호가 일치하지 않습니다")
        if len(password) < 8:
            return render_template('signup.html', error="비밀번호는 최소 8자 이상이어야 합니다")

        # 이메일 중복 검사
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="이미 가입된 이메일입니다")

        # 데이터베이스에 사용자 저장
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))  # 로그인 페이지로 이동
    
    return render_template('signup.html')

# HTML: 사용자 로그인
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # 세션 생성
            session['user_id'] = user.id
            session['user_name'] = user.username
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error="이메일 또는 비밀번호가 잘못되었습니다")
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()  # 세션 종료
    return redirect(url_for('main.home'))

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/checklist')
def checklist():
    return render_template('checklist.html')

@main.route('/ethical-consumption')
def ethical_consumption():
    return render_template('ethical_consumption.html')

@main.route('/budget', methods=["GET", "POST"])
def budget():
    if 'user_id' not in session:
        return render_template('budget.html')  # 로그인 전 화면
    else:
        user_data = get_user_data(session['user_id'])  # 로그인 후 사용자 데이터
        return render_template('budget.html', user_data=user_data)

@main.route('/add-travel', methods=['GET', 'POST'])
def add_travel():
    if request.method == 'POST':
        # 폼에서 전송된 데이터 가져오기
        travel_name = request.form.get('travel-name')
        country = request.form.get('country')
        region = request.form.get('region')
        budget = request.form.get('budget-won')
        
        # 유효성 검사
        if not travel_name or not country or not budget:
            error_message = "모든 필수 정보를 입력해주세요."
            return render_template('add_travel.html', error=error_message)

        # 데이터베이스에 저장
        new_travel = Travel(name=travel_name, country=country, region=region, budget=int(budget))
        db.session.add(new_travel)
        db.session.commit()

        success_message = "여행 일정이 성공적으로 추가되었습니다!"
        return render_template('budget.html', success=success_message)
    
    return render_template('add_travel.html')
