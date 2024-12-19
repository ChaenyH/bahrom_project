from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash
from app.main.models import db, User, Travel
from datetime import datetime
from . import main
import os
import google.generativeai as genai
import markdown
from flask import Markup


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

        print(f"Saved Data: username={username}, email={email}, password={password}")

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
            '중국': 'CNY',
            '영국': 'GBP',
            '호주': 'AUD',
            '베트남': 'VND',
            '태국': 'THB',
            '필리핀': 'PHP',
            '싱가포르': 'SGD',
            '대만': 'NTD',
            '인도네시아': 'IDR',
            '홍콩': 'HKD',
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

        print(f"Saved Data: travel_name={travel_name}, country={country}, region={region}, budget_won={int(budget_won)}, currency={currency}, budget_exchanged={0}, user_id={session['user_id']}")

        # POST 요청 후 리다이렉트
        return redirect(url_for('main.budget'))  # PRG 패턴 적용
    
    return render_template('add_travel.html')

@main.route('/add-consumption', methods=['GET', 'POST'])
def add_consumption():
    return render_template('add_consumption.html')

@main.route('/chatbot')
def chatbot():
    if 'user_id' not in session:  # 세션에 사용자 ID가 없으면 로그인 필요
        return redirect(url_for('main.login'))  # 로그인 페이지로 리다이렉트
    return render_template('chatbot.html')  # 로그인된 상태에서만 챗봇 페이지 렌더링

@main.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    if 'user_id' not in session:  # 세션 체크
        return jsonify({"error": "Unauthorized"}), 401

    user_input = request.json.get('message')  # 클라이언트로부터 메시지 수신
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # .env에서 GEMINI_API_KEY 가져오기
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return jsonify({"error": "GEMINI API Key not configured"}), 500

    # Gemini API 초기화
    genai.configure(api_key=gemini_api_key)

    # 사용자 데이터 가져오기
    user_data = get_user_data(session['user_id'])
    if not user_data:
        return jsonify({"error": "User data not found"}), 404

    # 맥락과 말투를 지정하는 프롬프트
    system_prompt = f"""
    너는 윤리적 소비 도우미 '띵곰이'야. 우리 서비스 이용자인 {user_data['username']}님에게 윤리적 소비와 관련된 구체적이고 실용적인 답변을 제시해줘.
    나처럼 반말을 사용해서 친근하지만 무례하지 않은 말투로 답해줘. 지시하는 듯한 어조는 지양하고, 권유하고 독려하는 어조를 사용해줘.
    만약 윤리적 소비와 전혀 관련 없는 질문을 했다면, 적당히 둘러대며 답변을 회피해줘.
    답변은 최대 300자 이내로 부탁할게.
    """

    # 프롬프트 조합
    full_prompt = f"""
    {system_prompt}
    
    띵곰이: 안녕? 나는 {user_data['username']}의 윤리적 소비를 도우러 온 띵곰이야. 소비와 관련해서 궁금한게 있다면 뭐든 답해줄게!
    
    사용자: {user_input}
    
    띵곰이: 
    """

    # 모델 생성 및 설정
    generation_config = {
        "temperature": 1,  # 생성 다양성
        "top_p": 0.95,  # 생성될 단어의 선택 폭
        "top_k": 40,  # 생성될 단어의 후보군
        "max_output_tokens": 500,  # 응답 길이 제한
        "response_mime_type": "text/plain",  # 응답의 형식
    }

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # 대화 세션 시작
        chat_session = model.start_chat(history=[])

        # 메시지 전송 및 응답 받기
        response = chat_session.send_message(full_prompt)

        markdown_html = markdown.markdown(response.text)

        return jsonify({"response": Markup(markdown_html)})
    except Exception as e:
        return jsonify({"error": f"Gemini API Error: {str(e)}"}), 500
