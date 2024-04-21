from flask import Flask, render_template, redirect
from data import session
from data.positions import Position
import datetime
from flask_login import LoginManager, login_user
from forms.position import PositionForm

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'my_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
session.global_init("db/menu.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = session.create_session()
    return db_sess.query(Position).get(user_id)


@app.route('/menu')
def menu():
    db_sess = session.create_session()
    position1 = db_sess.query(Position)

    return render_template('menu.html', position=position1)


@app.route('/basket')
def basket():
    return render_template('basket.html')


@app.route('/')
def add_position_in_basket():
    db_sess = session.create_session()
    for position_1 in db_sess.query(Position).all():
        if ... == position_1.name:
            return ...


@app.route('/position', methods=['GET', 'POST'])
def position():
    form = PositionForm()
    if form.validate_on_submit():
        db_sess = session.create_session()

        user = Position(
            name=form.name.data,
            price=form.price.data,
            about=form.about.data
        )
        db_sess.add(user)
        db_sess.commit()

        return redirect('/menu')

    return render_template('position.html', title='Добавление блюда', form=form)


@app.route('/')
def name():
    return "УРАА НАКОНЕЦТО!!!!"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
