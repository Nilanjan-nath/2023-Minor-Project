from flask import Flask, render_template, Blueprint,redirect, flash,request,session , url_for
from flask_login import login_required,login_user, logout_user
from .models import User
from .extensions import db
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint("auth", __name__)

@auth.route('/login', methods =["GET","POST"])
def login():
    if request.method =="POST":
        email = request.form["myEmail"]
        password = request.form["masterPassword"]

        logged_user = User.query.filter_by(email=email).first()
        if not logged_user or not check_password_hash(logged_user.password, password):
            flash("Please check your login details and try again")
            return redirect(url_for('auth.login'))

       
    
        flash("Logged in successfully",category="success")
        return redirect("/")

    return render_template("login.html")

@auth.route('/SignUp', methods=["GET", "POST"])
def signUp():
    if request.method =="POST":
        firstName = request.form["first_name"]
        lastName = request.form["last_name"]
        email = request.form["myEmail"]
        password = request.form["masterPassword"]
        
        newUser = User.query.filter_by(email=email).first()
        if newUser:
            flash("Acoount already exist! Please login to continue")
            return redirect(url_for("auth.login"))
        
        newUser = User(first_name = firstName , last_name = lastName , email = email, password = generate_password_hash(password ,method='sha256'))
        db.session.add(newUser)
        db.session.commit()
        flash("Account created Successfully! You can now log in ", category ="success")
        return redirect(url_for("login"))
        


    return render_template('signup.html')