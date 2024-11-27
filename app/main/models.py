from app import db  # app/__init__.py에서 정의된 db 인스턴스를 가져옴

# 사용자 정보를 관리하는 데이터 모델
class User(db.Model):
    from sqlalchemy import CheckConstraint
    from datetime import datetime, timezone

    id = db.Column(db.Integer, primary_key=True)  # 고유 식별자
    name = db.Column(db.String(100), nullable=False)  # 사용자 이름
    email = db.Column(db.String(120), unique=True, nullable=False)  # 이메일 주소(고유)
    __table_args__ = (
        CheckConstraint("email LIKE '%@%.%'", name='valid_email_check'),  # 이메일 유효성 검증
        )
    # 비밀번호를 해싱하여 데이터베이스에 저장합니다.
    # 해싱은 보안 강화를 위해 평문 비밀번호를 저장하지 않도록 합니다.
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # UTC 시간 저장 (사용자 생성 시간)

    # 사용자별 지출 데이터를 연결하기 위해 Expense 모델과 관계를 정의:
    expenses = db.relationship('Expense', backref='user', lazy='joined')

    # 비밀번호 설정 메서드
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        # generate_password_hash(password)는 주어진 비밀번호를 안전하게 해싱합니다.
        self.password_hash = generate_password_hash(password)

    # 비밀번호 검증 메서드
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        # check_password_hash(stored_hash, password)는 저장된 해시와 입력된 비밀번호를 비교합니다.
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}, Registered on {self.created_at}>"

# 지출 정보를 관리하는 데이터 모델
class Expense(db.Model):
    from datetime import date
    from sqlalchemy import Enum

    id = db.Column(db.Integer, primary_key=True)  # 고유 식별자
    # 날짜 데이터를 다룰 때는 String보다 Date 타입을 사용하는 것이 더 적합
    date = db.Column(db.Date, nullable=False)  # 지출 날짜
    category = db.Column(db.Enum(  # 지출 카테고리
        'Food', 'Transport', 'Shopping', 'Other', name='expense_category'  # 카테고리 제한
        ), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # 지출 금액
    memo = db.Column(db.String(200))  # 메모(선택 사항)
    
    # 사용자와 지출 간의 관계를 정의:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # __repr__ 메서드는 디버깅 및 로깅 시 객체를 명확히 식별하는 데 유용합니다.
    # 필요에 따라 더 많은 정보를 포함할 수도 있습니다.
    def __repr__(self):
        return f'<Expense {self.id}: {self.date} - {self.category} - {self.amount}>'
