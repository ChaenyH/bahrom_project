from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # SQLAlchemy 인스턴스 생성

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)  # Flask 앱에 데이터베이스 초기화

    # 블루프린트 등록
    from .routes import main
    app.register_blueprint(main)

    return app
