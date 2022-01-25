from flask import Flask
from flask_admin import Admin
import flask_login as login
from flask_admin.contrib.sqla import ModelView
from flask_login.utils import login_user, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/pashabank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

from extensions import *
from controllers import *
from models import *

if __name__ == '__main__':
    app.init_app(db)
    app.init_app(migrate)
    app.run(port=5000, debug=True)

def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if(user_id == "1"):
            return User(id=1,username="admin",password="123456")
        else :
            return False


class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_active and login.current_user.id == 1


init_login()
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(MyModelView(Slider, db.session))
admin.add_view(MyModelView(Cards, db.session))
admin.add_view(MyModelView(Subcard, db.session))
admin.add_view(MyModelView(Services, db.session))
admin.add_view(MyModelView(Subservice, db.session))
admin.add_view(MyModelView(Press, db.session))
admin.add_view(MyModelView(Bulleten, db.session))
admin.add_view(MyModelView(Hour, db.session))




