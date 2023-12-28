from flask import Flask, render_template, url_for, redirect, request, flash
from .extensions import db, login_manager
from .models import PasswordManager, User
from flask_login import login_required
from .auth import auth
from flask_migrate import Migrate
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def createapp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppmanager2.db'
    app.config['SQLALCHEMY_BINDS'] = {
        'keymanager': 'sqlite:///keyManager.db'
    }
    app.config['SECRET_KEY'] = 'mysecretkey'
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(auth, url_prefix='/')

    
    class AESCipher:
        def __init__(self, key):
            self.key = key

        def encrypt(self, raw):
            raw = pad(raw.encode('utf-8'), AES.block_size)
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        def decrypt(self, enc):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size).decode('utf-8')

    @app.route('/')
    def home():
        user_list = PasswordManager.query.all()
        return render_template("index.html", user_list=user_list)

    @app.route('/add', methods=["GET", "POST"])
    def add_details():
        if request.method == "POST":
            email = request.form["email"]
            site_password = request.form["site_password"]
            secret_key = get_random_bytes(16)
            aes_cipher = AESCipher(secret_key)
            encrypted_password = aes_cipher.encrypt(site_password)
            site_name = request.form["site_name"]

            user = PasswordManager(email=email, site_password=encrypted_password, site_name=site_name)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("home"))

    @app.route('/update/<int:id>', methods=["GET", "POST"])
    def update_details(id):
        updated_details = PasswordManager.query.filter_by(id=id).first()
        if request.method == "POST":
            updated_details.email = request.form["email"]
            secret_key = get_random_bytes(16)
            aes_cipher = AESCipher(secret_key)
            updated_details.site_password = aes_cipher.encrypt(request.form["site_password"])
            updated_details.site_name = request.form["site_name"]
            db.session.commit()
            return redirect(url_for("home"))
        return render_template("update.html", updated_details=updated_details)

    @app.route('/delete/<int:id>', methods=["GET", "POST"])
    def delete_details(id):
        details_to_delete = PasswordManager.query.filter_by(id=id).first()

        if details_to_delete:
            db.session.delete(details_to_delete)
            db.session.commit()
            flash("Site deleted successfully", category="success")
            return redirect(url_for("home"))
        else:
            flash("Some error has occurred")
            return render_template("index.html")

    with app.app_context():
        db.create_all()
        db.create_all(bind_key='keymanager')

    return app
