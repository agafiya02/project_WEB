from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PositionForm(FlaskForm):
    name = StringField('Название блюда', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    about = StringField("Ссылка на фото")
    submit = SubmitField('Сохранить')
