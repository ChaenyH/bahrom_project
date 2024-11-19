from app import create_app, db

app = create_app()

# 데이터베이스 생성 명령
@app.cli.command('create-db')
def create_db():
    """Create the database."""
    db.create_all()
    print("Database created!")

if __name__ == '__main__':
    # host와 port를 명시적으로 설정
    app.run(host="127.0.0.1", port=8080, debug=True)
