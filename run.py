from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # 데이터베이스 테이블 생성

# 디버깅용: 등록된 라우트 출력
print("Registered Routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
