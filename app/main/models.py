from app import db  # app/__init__.py에서 정의된 db 인스턴스를 가져옴

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    memo = db.Column(db.String(200))

    def __repr__(self):
        return f'<Expense {self.id}: {self.category} - {self.amount}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"