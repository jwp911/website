from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import test_user

#Defines forms for registering new users. Sets requirements such as
    #a section not being allowed to be empty, length constraints, formatting rules, etc.
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                             validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    #Allows checking if username is already registered before error occurs
    def validate_username(self, username):
        user = test_user.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    #Allows checking if email is already registered before error occurs
    def validate_email(self, email):
        user = test_user.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                             validators = [DataRequired()])

    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log-in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators = [DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators = [FileAllowed(['JPG', 'PNG', 'jpg', 'png', 'jpeg'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = test_user.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = test_user.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = test_user.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account associated with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')

