
from store import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(20), nullable=False)
    last_name= db.Column(db.String(20), nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    phone_number= db.Column(db.Integer, nullable=False)
    password= db.Column(db.String(60), nullable=False)
    su= db.Column(db.Boolean, default=False)
    is_banned= db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, index=True,
        default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.firstName} {self.lastName}', {self.email}, SU:[{self.su}])"

class UserView(ModelView):
    create_modal= True
    edit_modal= True
    column_searchable_list= ['email', 'is_banned']

admin.add_view(UserView(User, db.session))
