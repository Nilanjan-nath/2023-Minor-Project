from flask import Flask , render_template , request , url_for, blueprints , redirect ,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ppmanager.db"
app.config["SECRET_KEY"]="RALFJALASLSDF"

db=SQLAlchemy(app)


#model/schema for data
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(20), unique=False, nullable=False )
    site_password = db.Column(db.String(20),unique=False,nullable=False)
    site_name = db.Column(db.String(220), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' %self.email
    
with app.app_context():
    db.create_all()




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
        



if __name__ == '__main__':
    app.run(debug=True)