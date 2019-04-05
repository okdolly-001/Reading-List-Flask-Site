from flask import Flask, redirect, url_for
# Working with Blueprints
from model.readinglist import readinglist
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.api import api
from model.auth import auth
from database_setup import User, Base

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.show_login'
login_manager.login_message_category = "warning"

# A blueprint defines a collection of views, templates and static assets.
# See: https://danidee10.github.io/2016/11/20/flask-by-example-8.html
app.register_blueprint(readinglist)
app.register_blueprint(auth)
app.register_blueprint(api)


@app.route('/')
def main():
    """ Direct to book categories page """
    return redirect(
        url_for('readinglist.showBookCategories'))


@login_manager.user_loader
def load_user(user_id):
    """ """
    engine = create_engine('sqlite:///readinglist.db',
                           connect_args={'check_same_thread': False})
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(User).get(int(user_id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    login_manager.init_app(app)
    app.run(host='0.0.0.0', port=5000)
