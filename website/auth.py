from flask import Flask, render_template, Blueprint,redirect, flash,request,session
from flask_login import login_required
from .models import User
from .extensions import db


auth = Blueprint("auth", __name__)

@auth.route('/login', methods =["GET","POST"])
def login():
    if request.method =="POST":
        email = request.form["myEmail"]
        password = request.form["masterPassword"]

        logged_user = User(email=email , password = password)
        db.session.add(logged_user)
        db.session.commit()
        flash("Logged in successfully",category="success")
        return redirect("/")

    return render_template("login.html")

@auth.route('/SignUp')
def signUp():
    return render_template('signup.html')