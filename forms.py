from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm (FlaskForm) :
    name = StringField('Name',
                           validators=[DataRequired()])
    surname = StringField('Surname',
                       validators=[DataRequired()])
    id = StringField('Identity Card',
                           validators=[DataRequired()])
    img = FileField('Image ID',
                    validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                          validators=[DataRequired(), Email()])
    password= PasswordField('Password',
                          validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')



class LoginForm (FlaskForm) :

    email = StringField('Email',
                          validators=[DataRequired(), Email()])
    password= PasswordField('Password',
                          validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')