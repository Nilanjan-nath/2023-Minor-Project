from flask import Flask, render_template, url_for,redirect, request, flash

from .extensions import db,login_manager
from .models import PasswordManager, User
from flask_login import login_required

def createapp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppmanager2.db'
    app.config['SECRET_KEY'] = 'mysecretkey'
    db.init_app(app)


    @app.route('/')
    def home():
        user_list = PasswordManager.query.all()
        return render_template("index.html", user_list = user_list)

    @app.route('/add', methods =["GET", "POST"])

    def add_details():
        if request.method == "POST":
            email = request.form["email"]
            site_password = request.form["site_password"]
            site_name = request.form["site_name"]
            user = PasswordManager(email = email, site_password = site_password, site_name = site_name)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("home"))
        

    
    @app.route('/update/<int:id>',methods = ["GET", "POST"])
    def update_details(id):
        updated_details = PasswordManager.query.filter_by(id=id).first()
        if request.method=="POST":
        
                updated_details.email =request.form["email"]
                updated_details.site_password =request.form["site_password"]
                updated_details.site_name =request.form["site_name"]
                db.session.commit()
                return redirect(url_for("home"))
        return render_template("update.html", updated_details = updated_details)


    @app.route('/delete/<int:id>', methods=["GET","POST"])
    def delete_details(id):
        details_to_delete =PasswordManager.query.filter_by(id=id).first()
    
        if details_to_delete:
                db.session.delete(details_to_delete)
                db.session.commit()
                flash("Site deleted successfully",category="success")
                return redirect(url_for("home"))

        else:
            flash("Some error has occurred")
            return render_template("index.html")
    
    
    with app.app_context():
         db.create_all()
    
    return app