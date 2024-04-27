from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class PositionForm(FlaskForm):
    name = StringField('Название позиции', validators=[DataRequired()])
    price = StringField('цена позиции', validators=[DataRequired()])
    img = StringField("Ссылка на фото")
    about = StringField("Выберите категорию(Напитки или завтраки)")
    submit = SubmitField('Сохранить')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
