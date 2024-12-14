### 이 파일은 애플리케이션의 전역 설정 및 초기화를 담당합니다. 
### 즉, Flask 앱을 생성하고, 확장(extension)을 초기화하며, 블루프린트를 등록하는 역할을 합니다.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api.users import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app