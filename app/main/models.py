from app import db  # app/__init__.py에서 정의된 db 인스턴스를 가져옴
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM

# 사용자 정보를 관리하는 데이터 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 식별자
    username = db.Column(db.String(10), nullable=False)  # 사용자 이름
    email = db.Column(db.String(120), unique=True, nullable=False)  # 이메일 주소(고유)
    __table_args__ = (
        CheckConstraint("email LIKE '%@%.%'", name='valid_email_check'),  # 이메일 유효성 검증
        )
    # 비밀번호를 해싱하여 데이터베이스에 저장
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # UTC 시간 저장 (사용자 생성 시간)

    # 사용자별 지출 데이터를 연결하기 위해 Expense 모델과 관계를 정의
    travels = db.relationship('Travel', backref='user', lazy='joined')
    expenses = db.relationship('Expense', backref='user', lazy='joined')

    # 비밀번호 설정 메서드
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    # 비밀번호 검증 메서드
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.name}, Registered on {self.created_at}>"

# 여행 정보를 관리하는 데이터 모델
class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel_name = db.Column(db.String(80), nullable=False)
    country = db.Column(ENUM('한국', '미국', '유럽', '일본', '베트남', '대만', name='country_types'), nullable=False)
    region = db.Column(db.String(80), nullable=True, default="")
    budget_won = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)  # ISO 4217 코드 (예: KRW, USD)
    budget_exchanged = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Travel {self.id}: {self.travel_name} - {self.country} - {self.budget_won}>'

# 지출 정보를 관리하는 데이터 모델
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 고유 식별자
    date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    category = db.Column(ENUM('식비', '교통', '숙박', '관광', '쇼핑', '기타', name='expense_category'), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # 지출 금액
    payment_method = db.Column(db.String(20), nullable=False)  # 결제 수단 (현금, 카드 등)
    memo = db.Column(db.String(200), nullable=True)  # 메모(선택 사항)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # __repr__ 메서드는 디버깅 및 로깅 시 객체를 명확히 식별하는 데 유용합니다.
    # 필요에 따라 더 많은 정보를 포함할 수도 있습니다.
    def __repr__(self):
        return f'<Expense {self.id}: {self.date} - {self.category} - {self.amount}>'
