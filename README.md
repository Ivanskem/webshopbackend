database init
### flask db init
### flask db migrate -m "Initial migration"
### flask db upgrade

admin
from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('adminpassword')
    db.session.add(admin)
    db.session.commit()


run
python run.py