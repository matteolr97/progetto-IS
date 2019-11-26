from app import User,Travel
from app import db

with app.test_request_context():
    db.init_app(app)

    db.create_all()

user_1 = User(username='Matteo', email='matteo@gmail.com', password='1234')
db.session.add(user_1)