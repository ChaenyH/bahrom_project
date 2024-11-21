from flask import Blueprint

main = Blueprint('main', __name__)  # 'main'이라는 이름의 블루프린트 생성

from . import routes  # routes.py에서 라우트 로드
