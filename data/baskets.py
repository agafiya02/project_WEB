import sqlalchemy
from flask_login import UserMixin
from .session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Basket(SqlAlchemyBase, UserMixin):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    summ = sqlalchemy.Column(sqlalchemy.Integer)