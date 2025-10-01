from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, Regexp, ValidationError
from market.models import User

# We specify FlaskForm in the class definition because it makes our class inherit all the functionality of Flask-WTF forms.
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        matched_user = User.query.filter_by(username = username_to_check.data).first()
        if matched_user :
            raise ValidationError('User already exists!! Please try again with another username')
        
    def validate_email_address(self, email_address_to_check) :
        matched_email = User.query.filter_by(email_address = email_address_to_check.data).first()
        if matched_email:   # means if matched_email exists
            raise ValidationError('This email is already registered! Try with another email ID')

    username = StringField(label='User Name :', validators=[DataRequired(),Length(min=5, max=30), Regexp(r'^[a-zA-Z_]*$', message='Only letters, numbers, underscores')])
    email_address = StringField(label='Email Address :', validators=[DataRequired(), Email()])
    password1 = PasswordField(label='Password :', validators= [DataRequired(), Length(min=6)])
    password2 = PasswordField(label='confirm password :', validators = [DataRequired(), EqualTo('password1', message='password must match')])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm) :
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')