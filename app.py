from flask import Flask , render_template , request , url_for, blueprints
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ppmanager.db"
app.config["SECRET_KEY"]="RALFJALASLSDF"

db=SQLAlchemy(app)

with app.app_context():
    db.create_all()

#model/schema for data
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(20), unique=False, nullable=False )
    site_password = db.Column(db.String(20),unique=False,nullable=False)
    site_name = db.Column(db.String(220), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' %self.email



@app.route('/')
def helloWorld():
    return render_template("index.html")

@app.route('/add', methods =["GET", "POST"])

def add_details():
    if request.method == "POST":
        email = request.form["email"]
        site_password = request.form["site_password"]
        site_name = request.form["site_name"]
        
    return "adding Hello world"


@app.route('/update')
def update_details():
    return "Hello world"


@app.route('/delete')
def delete_details():
    return "Hello world"



if __name__ == '__main__':
    app.run(debug=True)