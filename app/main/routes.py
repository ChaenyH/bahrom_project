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

@main.context_processor
def inject_user():
    if 'user_id' in session:
        # 세션에 사용자 ID가 있으면 데이터베이스에서 사용자 정보 가져오기
        user_data = get_user_data(session['user_id'])
    else:
        # 로그인되지 않은 경우 None 반환
        user_data = None

    return {'user_data': user_data}

@main.route('/')
def home():
    return render_template('index.html')  # 로그인 전 화면

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
        return render_template('budget.html')  # 로그인 전 화면

@main.route('/add-travel', methods=['GET', 'POST'])
def add_travel():
    if request.method == 'POST':
        # 폼에서 전송된 데이터 가져오기
        travel_name = request.form.get('travel-name')
        country = request.form.get('country')
        region = request.form.get('region')
        budget_won = request.form.get('budget-won')

        # 국가에 따른 화폐 자동 매핑
        COUNTRY_TO_CURRENCY = {
            '한국': 'KRW',
            '미국': 'USD',
            '유럽': 'EUR',
            '일본': 'JPY',
            '베트남': 'VND',
            '대만': 'NTD'
        }
        currency = COUNTRY_TO_CURRENCY.get(country)
        
        # 유효성 검사
        if not travel_name or not country or not budget_won:
            error_message = "모든 필수 정보를 입력해주세요."
            return render_template('add_travel.html', error=error_message)

        existing_travel = Travel.query.filter_by(
            travel_name=travel_name,
            user_id=session['user_id']
        ).first()

        if existing_travel:
            error_message = "이미 존재하는 이름입니다."
            return render_template('add_travel.html', error=error_message)

        # 데이터베이스에 저장
        new_travel = Travel(
            travel_name=travel_name,
            country=country,
            region=region,
            budget_won=int(budget_won),
            currency=currency,
            budget_exchanged=0,  # 환율 변환된 예산은 이후 계산 가능
            user_id=session['user_id']
        )
        db.session.add(new_travel)
        db.session.commit()

        # POST 요청 후 리다이렉트
        return redirect(url_for('main.budget'))  # PRG 패턴 적용
    
    return render_template('add_travel.html')
