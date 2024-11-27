import os

# 현재 파일의 절대 경로를 기준으로 프로젝트 디렉토리의 경로를 설정합니다.
# 이후 파일 경로를 생성할 때 이 경로를 기준으로 사용할 수 있습니다.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 애플리케이션의 설정 값을 담고 있는 클래스입니다.
# Flask의 기본 설정 방식과 호환되며, 필요한 설정 값을 추가하거나 수정할 수 있습니다.
class Config:
    # Flask 애플리케이션의 비밀 키입니다.
    # CSRF(Cross-Site Request Forgery) 방지 및 세션 보안을 위해 사용됩니다.
    # 환경 변수 SECRET_KEY에서 값을 가져오며, 값이 없을 경우 기본값 'your_secret_key'를 사용합니다.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # SQLAlchemy를 사용하는 데이터베이스 URI입니다.
    # 환경 변수 DATABASE_URL에서 값을 가져오며, 값이 없을 경우 기본값으로 
    # 프로젝트 디렉토리에 database.db라는 이름의 SQLite 데이터베이스 파일을 생성합니다.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")

    # SQLAlchemy의 이벤트 시스템에서 변경 사항을 추적할지 여부를 결정합니다.
    # 기본값을 False로 설정하여 성능을 최적화합니다. 변경 사항 추적은 필요하지 않은 경우가 많습니다.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---
# 추가 환경 변수 및 설정:
    # 디버그 모드 (DEBUG)
    # 로깅 설정 (LOGGING_CONFIG)
    # 이메일 설정 (MAIL_SERVER, MAIL_PORT 등)

# 다른 환경(개발, 테스트, 프로덕션)을 위한 설정 구분:
    # DevelopmentConfig, TestingConfig, ProductionConfig 등의 클래스를 만들어 
    # 환경별 설정을 따로 관리할 수 있습니다.
