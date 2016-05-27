# coding: utf-8

# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, SelectField, IntegerField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, NumberRange


# Define the login form (WTForms)

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password. ;-)')])

class DepositForm(Form):
    name     = SelectField('Name', choices=[])

    amount   = IntegerField('Amount', [NumberRange(min=1, max=10000, message=u"Částka musí být v rozmezí %(min)s a %(max)s Kč"),
		Required(message=u'Musíte vložit nějakou částku')])

class ShowPersonForm(Form):
    name     = SelectField('Name', choices=[])

