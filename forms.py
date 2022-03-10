from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class RegisterUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginUser(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ReportForm(FlaskForm):
    date_received = DateField("Date Received", validators=[DataRequired()])
    day_zero = DateField("Day Zero", validators=[DataRequired()])
    case_id = StringField("Case ID")
    case_version = SelectField("Case version", choices=["Initial", "Follow-up 1",
                                                        "Follow-up 2", "Follow-up 3",
                                                        "Follow-up 4", "Follow-up 5",
                                                        "Follow-up 6", "Follow-up 7"])
    other_case_id = StringField("Other Case IDs")
    drug = StringField("Drug", validators=[DataRequired()])
    serious = SelectField("Serious", choices=['Serious', 'Non-serious', 'N/A'])
    listed = SelectField("Listed", choices=['N/A', 'Listed', 'Unlisted'])
    expedited = BooleanField("Expedited to RA")
    exchange = BooleanField("Exchange with partners")
    comments = TextAreaField("Comments", validators=[Length(max=500)])
    submit = SubmitField("Add Report")


class AddTaskForm(FlaskForm):
    task_owner = SelectField("Responsible person", validators=[DataRequired()])
    task_name = SelectField("Task", choices=["Data Entry", "Quality Check",
                                             "Medical Review", "Submission to RA",
                                             "Exchange with Partners", "Case Finalization"])
    due_date = DateField("Due Date", validators=[DataRequired()])
    task_comments = TextAreaField("Comments", validators=[Length(max=500)])
    submit = SubmitField("Add Task")


class EditTaskForm(FlaskForm):
    task_owner = SelectField("Responsible person", validators=[DataRequired()])
    task_name = SelectField("Task", choices=["Data Entry", "Quality Check",
                                             "Medical Review", "Submission to RA",
                                             "Exchange with Partners", "Case Finalization"])
    due_date = DateField("Due Date", validators=[DataRequired()])
    completed = BooleanField("Completed")
    task_comments = TextAreaField("Comments", validators=[Length(max=500)])
    submit = SubmitField("Update Task")


class EditPasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Confirm")


class DeleteAccountForm(FlaskForm):
    confirm_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Confirm")

