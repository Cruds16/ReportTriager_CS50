from flask import Flask, render_template, request, redirect, flash
from forms import RegisterUser, LoginUser
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '45678this_is_just_testing_key_dont_get_excited0123'

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///triager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# USERS TABLE
class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    roles = db.Column(db.String(250))


# creates db
# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    register_form = RegisterUser()
    login_form = LoginUser()
    if request.method == "GET":
        return render_template("title.html", register_form=register_form, login_form=login_form)
    else:
        if register_form.validate_on_submit():

            if not register_form.password.data == register_form.confirm_password.data:
                flash("Passwords do not match")
                return render_template("title.html", register_form=register_form, login_form=login_form)

            if User.query.filter_by(username=register_form.username.data).first()\
                    or User.query.filter_by(email=register_form.email.data).first():
                flash("Username or email already registered")
                return render_template("title.html", register_form=register_form, login_form=login_form)

            new_user = User(username=register_form.username.data,
                            password=generate_password_hash(password=register_form.password.data,
                                                            method="pbkdf2:sha256",
                                                            salt_length=8),
                            email=register_form.email.data)
            db.session.add(new_user)
            db.session.commit()

            flash("User registration succesful")
            return render_template("title.html", register_form=register_form, login_form=login_form)

        elif login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if not user:
                flash("User does not exist, please register")
                return render_template("title.html", register_form=register_form, login_form=login_form)

            if not check_password_hash(pwhash=user.password, password=login_form.password.data):
                flash("Incorrect password")
                return render_template("title.html", register_form=register_form, login_form=login_form)

            load_user(user.id)
            login_user(user)

            return redirect("/dashboard")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)