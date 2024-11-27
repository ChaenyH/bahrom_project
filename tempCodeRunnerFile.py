# create_app은 Flask 애플리케이션 팩토리 함수로, 
# 애플리케이션 인스턴스를 생성하고 설정을 초기화하는 역할을 합니다.
# 이 방식은 애플리케이션 구조를 더 모듈화하고 테스트 가능하게 만듭니다.

# db는 SQLAlchemy 데이터베이스 객체입니다. 
# Flask-SQLAlchemy 확장을 통해 정의됩니다.
# 이를 통해 데이터베이스 관련 작업을 수행합니다.
from app import create_app, db

# create_app 함수 호출로 애플리케이션 인스턴스를 생성합니다.
# 일반적으로 create_app은 애플리케이션 설정, 확장 등록, 블루프린트 등록 등을 처리합니다.
app = create_app()

# Flask의 애플리케이션 컨텍스트를 활성화합니다. 
# 이 컨텍스트는 데이터베이스 작업과 같은 일부 작업에서 필요합니다.
with app.app_context():
    # 현재 정의된 SQLAlchemy 모델 기반으로 데이터베이스 테이블을 생성합니다.
    # 이는 초기 개발 단계나 테스트용으로 유용하며, 
    # 실제 배포 환경에서는 Flask-Migrate를 사용하는 것이 더 좋습니다.
    db.create_all()

if app.debug:
    # Flask 애플리케이션에 등록된 모든 라우트를 출력합니다.
    # 디버깅 시 유용하며, 등록된 URL 경로와 엔드포인트를 확인할 수 있습니다.
    print("Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

# host="127.0.0.1":
    # 로컬 호스트에서 실행되도록 설정합니다. 
    # 외부에서 접근하려면 "0.0.0.0"으로 변경해야 합니다.
# port=8080:
    # Flask 서버가 실행될 포트를 지정합니다.
# debug=True:
    # 디버그 모드를 활성화합니다. 이 모드는 코드 변경 시 자동으로 서버를 재시작하며, 디버깅 툴도 제공합니다.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

# ---
# 환경별 설정:
    # 개발, 테스트, 프로덕션 환경에 따라 app.run()의 매개변수(host, port, debug)를 변경하거나 
    # create_app에 설정을 전달할 수 있습니다.
# 데이터베이스 마이그레이션:
    # db.create_all() 대신 Flask-Migrate를 사용하면 
    # 데이터베이스 스키마 변경 시 더 안전하고 유연하게 관리할 수 있습니다.
# 라우트 자동 탐색:
    # print("Registered Routes:") 부분을 개선하여 
    # 엔드포인트 함수 이름, HTTP 메소드 등도 출력하도록 만들 수 있습니다.
