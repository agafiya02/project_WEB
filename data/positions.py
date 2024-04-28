import sqlalchemy
from flask_login import UserMixin
from .session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Position(SqlAlchemyBase, UserMixin):
    __tablename__ = 'menu'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    like = sqlalchemy.Column(sqlalchemy.String, default=0)
    dislike = sqlalchemy.Column(sqlalchemy.String, default=0)
