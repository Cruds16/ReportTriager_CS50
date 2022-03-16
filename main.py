from flask import Flask, render_template, request, redirect, flash
from forms import RegisterUser, LoginUser, ReportForm, AddTaskForm, EditTaskForm, EditPasswordForm, DeleteAccountForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("app-key")

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Configure db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///triager.db')
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
    # It also establishes a taskowner attribute on Task which will refer to the parent User object.
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
    task_comments = db.Column(db.String(500), nullable=True)


class Report(UserMixin, db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_received = db.Column(db.Date, nullable=True)
    day_zero = db.Column(db.Date, nullable=True)
    case_id = db.Column(db.String(250), nullable=True)
    case_version = db.Column(db.String(250), nullable=True)
    other_case_id = db.Column(db.String(250), nullable=True)
    drug = db.Column(db.String(250), nullable=True)
    serious = db.Column(db.String(250), nullable=True)
    listed = db.Column(db.String(250), nullable=True)
    expedited = db.Column(db.Boolean, nullable=True)
    exchange = db.Column(db.Boolean, nullable=True)
    comments = db.Column(db.String(500), nullable=True)

    # backref establishes a collection of Task objects on Report called report_tasks
    # It also establishes a .report attribute on Task which will refer to the parent Report object.
    report_tasks = db.relationship("Task", backref="report")


# creates db
db.create_all()


def return_error(message, code):
    return render_template("error.html", message=message, code=code), code


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
                return redirect("/")

            if User.query.filter_by(username=register_form.username.data).first()\
                    or User.query.filter_by(email=register_form.email.data).first():
                flash("Username or email already registered")
                return redirect("/")

            new_user = User(username=register_form.username.data,
                            password=generate_password_hash(password=register_form.password.data,
                                                            method="pbkdf2:sha256",
                                                            salt_length=8),
                            email=register_form.email.data)
            db.session.add(new_user)
            db.session.commit()

            flash("User registration successful")
            return redirect("/")

        elif login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if not user:
                flash("User does not exist, please register")
                return redirect("/")

            if not check_password_hash(pwhash=user.password, password=login_form.password.data):
                flash("Incorrect password")
                return redirect("/")

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
                            drug=report_form.drug.data,
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

    if not report:
        return return_error("Report does not exist", 404)

    report_details_form = ReportForm(date_received=report.date_received, day_zero=report.day_zero,
                                     case_id=report.case_id, case_version=report.case_version,
                                     other_case_id=report.other_case_id, drug=report.drug,
                                     serious=report.serious, listed=report.listed,
                                     expedited=report.expedited, exchange=report.exchange,
                                     comments=report.comments)
    report_details_form.submit.label.text = 'Update Report'

    report_task_form = AddTaskForm()

    user_list = User.query.all()
    user_choices = [(user.id, user.username) for user in user_list]

    report_task_form.task_owner.choices = user_choices

    report_tasks = Task.query.filter_by(report_id=id).all()

    if request.method == "GET":
        return render_template("report.html", form=report_details_form,
                               new_task=report_task_form,
                               report_tasks=report_tasks,
                               report_id=id)
    else:
        if report_details_form.validate_on_submit():
            report.date_received = report_details_form.date_received.data
            report.day_zero = report_details_form.day_zero.data
            report.case_id = report_details_form.case_id.data
            report.case_version = report_details_form.case_version.data
            report.other_case_id = report_details_form.other_case_id.data
            report.drug = report_details_form.drug.data
            report.serious = report_details_form.serious.data
            report.listed = report_details_form.listed.data
            report.expedited = report_details_form.expedited.data
            report.exchange = report_details_form.exchange.data
            report.comments = report_details_form.comments.data
            db.session.commit()

        if report_task_form.validate_on_submit():
            new_task = Task(taskowner_id=report_task_form.task_owner.data, report_id=id,
                            task_name=report_task_form.task_name.data, due_date=report_task_form.due_date.data,
                            completed=False, task_comments=report_task_form.task_comments.data)
            db.session.add(new_task)
            db.session.commit()
    return redirect(f"/report/{report.id}")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/delete_task/<task_id>")
@login_required
def delete_task(task_id):
    task_to_delete = Task.query.filter_by(id=task_id).first()

    if not task_to_delete:
        return return_error("Task does not exist", 404)

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/task_list")


@app.route("/complete_task/<task_id>")
@login_required
def complete_task(task_id):
    completed_task = Task.query.filter_by(id=task_id).first()

    if not completed_task:
        return return_error("Task does not exist", 404)

    completed_task.completed = True
    db.session.commit()
    return redirect(request.referrer)


@app.route("/delete_report/<report_id>")
@login_required
def delete_report(report_id):
    report_to_delete = Report.query.filter_by(id=report_id).first()

    if not report_to_delete:
        return return_error("Report does not exist", 404)

    db.session.delete(report_to_delete)
    db.session.commit()
    return redirect("/dashboard")


@app.route("/task_list")
@login_required
def task_list():
    your_tasks = Task.query.filter_by(taskowner_id=current_user.id, completed=False).all()
    all_ongoing_tasks = Task.query.filter_by(completed=False).all()
    all_completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template("task_list.html", your_tasks=your_tasks, all_ongoing_tasks=all_ongoing_tasks,
                           all_completed_tasks=all_completed_tasks)


@app.route("/task/<task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task_to_edit = Task.query.filter_by(id=task_id).first()

    if not task_to_edit:
        return return_error("Task does not exist", 404)

    # prepares unordered list of choices 'user_choices' for taskowner SelectField
    user_list = User.query.all()
    user_choices = [(user.id, user.username) for user in user_list]

    # check if taskowner exists (in case the account was deleted previously)
    if task_to_edit.taskowner_id:
        # Order user_list with the current taskowner at the first place
        # this works as pre-population of the field with the current taskowner name
        # 'person_index' keeps index of the current taskowner in unordered list 'user_choices'
        person_index = user_choices.index((task_to_edit.taskowner_id, task_to_edit.taskowner.username))
        # puts the current taskowner at the first place in the unordered list
        user_choices[0], user_choices[person_index] = user_choices[person_index], user_choices[0]
    else:
        user_choices.append(("", ""))
        user_choices[0], user_choices[-1] = user_choices[-1], user_choices[0]

    edit_task_form = EditTaskForm(task_name=task_to_edit.task_name,
                                  due_date=task_to_edit.due_date,
                                  task_comments=task_to_edit.task_comments,
                                  completed=task_to_edit.completed)

    edit_task_form.task_owner.choices = user_choices

    if request.method == "GET":
        return render_template("task.html", form=edit_task_form, task=task_to_edit)
    else:
        if edit_task_form.validate_on_submit():
            task_to_edit.task_name = edit_task_form.task_name.data
            task_to_edit.taskowner_id = edit_task_form.task_owner.data
            task_to_edit.due_date = edit_task_form.due_date.data
            task_to_edit.task_comments = edit_task_form.task_comments.data
            task_to_edit.completed = edit_task_form.completed.data
            db.session.commit()

        return redirect(f"/report/{task_to_edit.report_id}")


@app.route("/account_settings", methods=["GET", "POST"])
@login_required
def account_settings():
    edit_password_form = EditPasswordForm()
    delete_account_form = DeleteAccountForm()
    user = User.query.filter_by(id=current_user.id).first()

    if request.method == "GET":
        return render_template("account_settings.html", edit_password_form=edit_password_form,
                               delete_account_form=delete_account_form)
    else:
        if edit_password_form.validate_on_submit():
            if not check_password_hash(pwhash=user.password, password=edit_password_form.old_password.data):
                flash("Incorrect password")
                return redirect("/account_settings")
            elif not edit_password_form.new_password.data == edit_password_form.confirm_password.data:
                flash("Passwords do not match")
                return redirect("/account_settings")
            else:
                user.password = generate_password_hash(password=edit_password_form.new_password.data,
                                                       method="pbkdf2:sha256",
                                                       salt_length=8)
                db.session.commit()
                flash("Password updated")
                return redirect("/account_settings")

        if delete_account_form.validate_on_submit():
            if not check_password_hash(pwhash=user.password, password=delete_account_form.confirm_password.data):
                flash("Incorrect password")
                return redirect("/account_settings")
            else:
                db.session.delete(user)
                db.session.commit()
                flash("Account deleted")
                return redirect("/")


if __name__ == "__main__":

    app.run()

