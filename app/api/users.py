### RESTful API
# API 중심 설계로, 클라이언트-서버 통신(예: JSON)과 관련된 책임을 담당.
# JSON 요청/응답 처리.
# API는 HTML 렌더링에 의존하지 않고 데이터를 반환합니다.
# ---
from flask import Blueprint, jsonify, request
from app.main.models import User, db

api = Blueprint('api', __name__)

# API: 모든 사용자 목록 조회
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(user_list)

# API: 사용자 등록
@api.route('/register', methods=['POST'])
def register():
    data = request.json  # JSON 데이터 처리
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# API: 사용자 로그인
@api.route('/login', methods=['POST'])
def login():
    data = request.json  # JSON 데이터 처리
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
