from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email


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
    case_version = SelectField("Case version", choices=[("INI", "Initial"), ("FU1", "Follow-up 1"),
                                                        ("FU1", "Follow-up 1"), ("FU2", "Follow-up 2"),
                                                        ("FU3", "Follow-up 3"), ("FU4", "Follow-up 4"),
                                                        ("FU5", "Follow-up 5"), ("FU1", "Follow-up 6")])
    other_case_id = StringField("Other Case IDs")
    serious = BooleanField("Serious")
    listed = BooleanField("Listed")
    expedited = BooleanField("Expedited")
    exchange = BooleanField("Exchange with partners")
    comments = StringField("Comments")
    submit = SubmitField("Add Report")