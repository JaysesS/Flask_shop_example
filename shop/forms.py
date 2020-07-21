from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, ValidationError
from wtforms.validators import InputRequired, Email, Length, NumberRange

import phonenumbers

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired(), Length(min = 4, max = 20)])
    password = PasswordField("Password", validators = [InputRequired(), Length(min = 6, max = 30)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min = 4, max = 20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min = 6, max = 30)])
    email = StringField("Email", validators=[InputRequired(), Length(max=60), Email(message="Invalid email")])
    submit = SubmitField("Register")

class AccountForm(FlaskForm):
    phone = StringField('Phone', validators=[InputRequired()], description="Example: +79999999999")
    adress = StringField('Address', validators=[InputRequired(), Length(min = 15)], description="Example: Saint-Petersburg, Stachek square 7, 666")
    money = StringField('Money', validators=[InputRequired(), Length(min = 1)])
    submit = SubmitField('Submit')

    def validate_money(self, money):
        try:
            m = int(money.data)
            if m < 0:
                raise ValidationError('Money must be > 0')
        except ValueError:
            raise ValidationError('Money must be integer!')
        

    def validate_adress(self, adress):
        if len(set(list(adress.data))) == 0:
            raise ValidationError('Invalid adress.')
        elif adress.data.count(',') < 2:
            raise ValidationError('Invalid adress.')
    def validate_phone(self, phone):
        if len(phone.data) > 12:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            raise ValidationError('Invalid phone number.')