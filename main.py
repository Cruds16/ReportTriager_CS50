from flask import Flask, render_template, request, redirect, flash
from forms import RegisterUser, LoginUser, ReportForm, AddTaskForm
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
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)

    # backref establishes a collection of Task objects on User called user_tasks
    # It also establishes a .taskowner attribute on Task which will refer to the parent User object.
    user_tasks = db.relationship("Task", backref='taskowner')

# TASKS TABLE
class Task(UserMixin, db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    # Create Foreign Key : taskowner_id refers to the primary key "user.id" from the table 'user'
    taskowner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Create Foreign Key: "report_id" refers to the primary key "report.id" in the table 'report'
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))

    task_name = db.Column(db.String(500), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean(), nullable=True)
    comments = db.Column(db.String(500), nullable=True)


class Report(UserMixin, db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_received = db.Column(db.Date, nullable=True)
    day_zero = db.Column(db.Date, nullable=True)
    case_id = db.Column(db.String(250), nullable=True)
    case_version = db.Column(db.String(250), nullable=True)
    other_case_id = db.Column(db.String(250), nullable=True)
    serious = db.Column(db.String(250), nullable=True)
    listed = db.Column(db.String(250), nullable=True)
    expedited = db.Column(db.Boolean, nullable=True)
    exchange = db.Column(db.Boolean, nullable=True)
    comments = db.Column(db.String(500), nullable=True)

    # backref establishes a collection of Task objects on Report called report_tasks
    # It also establishes a .report attribute on Task which will refer to the parent Report object.
    report_tasks = db.relationship("Task", backref="report")

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

            flash("User registration successful")
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
    reports_table = Report.query.all()
    user_todos = Task.query.filter_by(taskowner_id=current_user.id).all()
    return render_template("dashboard.html", reports=reports_table, user_todos=user_todos)


@app.route("/new_report", methods=["GET", "POST"])
@login_required
def new_report():
    report_form = ReportForm()
    if request.method == "GET":
        return render_template("new_report.html", form=report_form)
    else:
        new_report = Report(date_received=report_form.date_received.data,
                            day_zero=report_form.day_zero.data,
                            case_id=report_form.case_id.data,
                            case_version=report_form.case_version.data,
                            other_case_id=report_form.other_case_id.data,
                            serious=report_form.serious.data,
                            listed=report_form.listed.data,
                            expedited=report_form.expedited.data,
                            exchange=report_form.exchange.data,
                            comments=report_form.comments.data)
        db.session.add(new_report)
        db.session.commit()

        return redirect("/dashboard")


@app.route("/report/<id>", methods=["GET", "POST"])
@login_required
def report(id):
    report = Report.query.filter_by(id=id).first()

    report_details_form = ReportForm(date_received=report.date_received, day_zero=report.day_zero,
                                     case_id=report.case_id, case_version=report.case_version,
                                     other_case_id=report.other_case_id, serious=report.serious,
                                     listed=report.listed, expedited=report.expedited,
                                     exchange=report.exchange, comments=report.comments)
    report_details_form.submit.label.text = 'Update Report'

    report_task_form = AddTaskForm()

    user_list = User.query.all()
    user_choices = [(user.id, user.username) for user in user_list]

    report_task_form.task_owner.choices = user_choices

    if request.method == "GET":
        return render_template("report.html", form=report_details_form, new_task=report_task_form)
    else:
        if report_details_form.validate_on_submit():
            report.date_received = report_details_form.date_received.data
            report.day_zero = report_details_form.day_zero.data
            report.case_id = report_details_form.case_id.data
            report.case_version = report_details_form.case_version.data
            report.other_case_id = report_details_form.other_case_id.data
            report.serious = report_details_form.serious.data
            report.listed = report_details_form.listed.data
            report.expedited = report_details_form.expedited.data
            report.exchange = report_details_form.exchange.data
            report.comments = report_details_form.comments.data
            db.session.commit()

        if report_task_form.validate_on_submit():
            new_task = Task(taskowner_id=report_task_form.task_owner.data, report_id=id,
                            task_name=report_task_form.task_name.data, due_date=report_task_form.due_date.data,
                            completed=False, comments=report_task_form.comments.data)
            db.session.add(new_task)
            db.session.commit()
    return redirect(f"/report/{report.id}")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)