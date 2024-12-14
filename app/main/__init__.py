### 이 파일은 main 블루프린트를 초기화하고, 해당 블루프린트에서 사용할 라우트와 모델 등을 연결합니다. 
### 이 블루프린트는 애플리케이션의 특정 기능(예: 메인 페이지, 로그인, 회원가입 등)을 관리합니다.

from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes