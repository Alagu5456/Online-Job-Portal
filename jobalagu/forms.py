from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=200)])
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    job_type = SelectField('Job Type', 
                          choices=[('Full-time', 'Full-time'), 
                                 ('Part-time', 'Part-time'), 
                                 ('Contract', 'Contract'), 
                                 ('Internship', 'Internship')],
                          validators=[DataRequired()])
    salary_range = StringField('Salary Range', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[Optional()])
    application_deadline = DateTimeField('Application Deadline', 
                                       format='%Y-%m-%d',
                                       validators=[Optional()])

class ApplicationForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[Optional()])
    resume = FileField('Upload Resume (PDF)', 
                      validators=[FileRequired(), 
                                FileAllowed(['pdf'], 'Only PDF files are allowed!')])

class ApplicationStatusForm(FlaskForm):
    status = SelectField('Status', 
                        choices=[('pending', 'Pending'), 
                               ('reviewed', 'Reviewed'), 
                               ('accepted', 'Accepted'), 
                               ('rejected', 'Rejected')],
                        validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])

class JobSearchForm(FlaskForm):
    search_term = StringField('Search Jobs', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    job_type = SelectField('Job Type', 
                          choices=[('', 'All Types'),
                                 ('Full-time', 'Full-time'), 
                                 ('Part-time', 'Part-time'), 
                                 ('Contract', 'Contract'), 
                                 ('Internship', 'Internship')],
                          validators=[Optional()])
