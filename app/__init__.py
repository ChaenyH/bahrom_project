# Flask: Flask 애플리케이션을 생성하는 데 사용됩니다.
from flask import Flask
# SQLAlchemy: Flask-SQLAlchemy 확장을 사용하여 데이터베이스를 관리합니다.
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask 애플리케이션에 데이터베이스 작업을 추가하기 위해 SQLAlchemy 객체를 생성합니다.
# 이 객체는 이후 app 인스턴스와 연결됩니다.
db = SQLAlchemy()

migrate = Migrate()

# 애플리케이션 팩토리 패턴을 사용합니다.
# 이 패턴은 모듈화와 테스트를 용이하게 합니다.
# Flask 인스턴스를 함수 내에서 생성하여 호출 시마다 새로운 애플리케이션 인스턴스를 반환합니다.
def create_app():
    app = Flask(__name__)

    # Config 클래스를 사용하여 애플리케이션 설정을 로드합니다.
    # 설정은 config.py 파일에 정의되어 있습니다.
    app.config.from_object('config.Config')

    # db 객체를 Flask 애플리케이션에 연결합니다.
    # 이 초기화 과정을 통해 데이터베이스 작업을 수행할 수 있습니다.
    db.init_app(app)

    migrate.init_app(app, db)  # 마이그레이션 초기화

    # main 블루프린트를 가져와 등록합니다. 
    # 이는 애플리케이션의 주요 라우트를 관리합니다.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # api 블루프린트를 가져와 /api 경로에 등록합니다. 
    # API와 관련된 라우트를 관리합니다.
    from .api.users import api as api_blueprint
    # url_prefix='/api'는 이 블루프린트의 모든 엔드포인트 앞에 /api가 추가되도록 설정합니다.
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

# ---
# 블루프린트 개념:
    # Flask에서 블루프린트는 애플리케이션 라우트, 뷰 함수, 기타 기능을 모듈화하여 관리할 수 있도록 합니다.
    # 이 코드에서 두 개의 블루프린트를 사용합니다:
        # main: 일반적인 웹 애플리케이션 라우트
        # api: REST API 관련 라우트

# 확장 가능성
    # 환경 구분 설정:
        # app.config.from_object('config.DevConfig') 또는 config.ProdConfig와 같은 방식으로 환경별 설정 클래스를 구분할 수 있습니다.
    # 추가 블루프린트:
        # 더 많은 기능(예: 관리자, 인증)을 위해 추가 블루프린트를 등록할 수 있습니다.
    # 에러 핸들링:
        # @app.errorhandler를 사용하여 전역 에러 핸들링을 추가할 수 있습니다.
    # Flask 확장 추가:
        # 예: Flask-Migrate, Flask-WTF, Flask-Login 등 추가 가능
