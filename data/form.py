from flask_wtf import FlaskForm
from wtforms import SubmitField


class Form(FlaskForm):
    menu = SubmitField('Войти')
    about_us = SubmitField('Войти')
    basket = SubmitField('Войти')
