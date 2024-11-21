from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Config 클래스에서 설정 로드
    app.config.from_object('config.Config')

    # SQLAlchemy 초기화
    db.init_app(app)

    # main 블루프린트 등록
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # api 블루프린트 등록
    from .api.users import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app