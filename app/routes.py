from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

project_templates = {
    1: {"template": "project_1_detail.html", "title": "윤리적 소비 가이드"},
    2: {"template": "project_2_detail.html", "title": "여행 계획 및 예산 관리"}
}

# ------------

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')  # 새로운 페이지 템플릿

@main.route('/projects')
def projects():
    return render_template('projects.html')  # 새로운 페이지 템플릿

@main.route('/projects/2')
def project_2_detail():
    # 추가 데이터가 필요하면 아래 딕셔너리를 수정하거나 템플릿으로 전달
    project_data = {
        "title": "여행 계획 및 예산 관리",
        "description": "효율적인 예산 관리와 윤리적인 소비를 돕는 여행 도구를 제공합니다."
    }
    return render_template("project_2_detail.html", project=project_data)

@main.route('/projects/<int:project_id>')
def project_detail(project_id):
    # 프로젝트 ID로 템플릿과 제목 조회
    project_info = project_templates.get(project_id)

    if not project_info:
        # ID가 유효하지 않을 경우 404 반환
        return render_template('404.html'), 404

    # 템플릿 렌더링
    return render_template(project_info["template"], project={"id": project_id, "title": project_info["title"]})

# ------------

@main.route('/api/users')
def get_users():
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    return jsonify(users)  # JSON 형식으로 응답

from flask import request
from .models import User, db

@main.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully", "user": {"name": name, "email": email}}), 201
