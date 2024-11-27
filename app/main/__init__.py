# Blueprint는 Flask 애플리케이션을 모듈화하고 구조적으로 관리하기 위한 기능입니다.
from flask import Blueprint

# main이라는 이름의 블루프린트를 생성하며, 해당 블루프린트는 애플리케이션의 기본 라우트를 담당합니다.
# __name__은 현재 모듈의 이름을 전달하여 Flask가 이 블루프린트를 찾을 수 있도록 합니다.
main = Blueprint('main', __name__)

# routes 모듈을 가져와 블루프린트에 라우트를 등록합니다.
# routes.py 파일에는 이 블루프린트와 연결된 URL 경로와 해당 경로를 처리하는 뷰 함수가 정의되어 있을 것입니다.
# from . import routes는 현재 디렉토리에서 routes.py를 가져오는 구문입니다.
from . import routes

# ---
# 확장 가능성
    # 블루프린트 URL Prefix 추가:
        # Blueprint를 생성할 때 url_prefix='/main'과 같이 URL 접두사를 설정할 수 있습니다.
        # 모든 경로가 /main으로 시작하도록 만들 수 있습니다.
    # 라우트 분리:
        # routes.py에서 라우트를 명확하게 분리하여 읽기 쉽고 관리하기 쉽게 만들 수 있습니다.
        # 예를 들어, 특정 라우트는 별도의 파일로 분리할 수도 있습니다.
    # 에러 핸들러 추가:
        # 블루프린트 레벨에서 에러 핸들링을 추가할 수 있습니다.