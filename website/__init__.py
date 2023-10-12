from flask import Flask
from flask import Blueprint
def createapp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASDASDFLKJADSF LKJKL'

    from .views import views
    app.register_blueprint(views, url_prefix=("/"))

    return app
