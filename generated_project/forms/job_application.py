from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email

class JobApplicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    application_status = SelectField('Application Status', choices=[('new', 'New'), ('pending', 'Pending'), ('approved', 'Approved')], coerce=str)
    submit = SubmitField('Submit')