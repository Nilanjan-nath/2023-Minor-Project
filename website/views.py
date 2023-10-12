from flask import Blueprint, render_template , request, Flask
from . import createapp
app = createapp()

views = Blueprint('views', __name__)
@views.route("/")
def home():
    return render_template("index.html")