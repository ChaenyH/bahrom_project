import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask 애플리케이션의 비밀 키 (환경 변수로부터 가져오거나 기본값 설정)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # SQLAlchemy 데이터베이스 URI (기본값: 프로젝트 디렉토리에 SQLite 데이터베이스 파일 생성)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")

    # SQLAlchemy 설정: 변경 사항을 추적하지 않도록 설정 (성능 최적화)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
