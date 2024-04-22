from flask import Flask, render_template, redirect, abort
from data import session
from data.positions import Position
import datetime
from data.users import User
from flask_login import LoginManager, login_user, login_required
from forms.user import RegisterForm, LoginForm, PositionForm

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'my_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
session.global_init("db/user.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = session.create_session()
    return db_sess.query(Position).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/menu')
def menu():
    # <a href="{{ url_for('add_position_in_basket') }}" class="btn btn-warning btn-lg">
    db_sess = session.create_session()
    position1 = db_sess.query(Position)

    return render_template('menu.html', position=position1)


@app.route('/logout')
@login_required
def logout():
    return redirect("/")


@app.route('/basket')
def basket():
    return render_template('basket.html')


# def add_position_in_basket():
# db_sess = session.create_session()
# for position_1 in db_sess.query(Position).all():
#  if position_1.name == ...:
#   return ...


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


@app.route('/position_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = session.create_session()
    position1 = db_sess.query(Position).filter(Position.id == id).first()
    if position1:
        db_sess.delete(position1)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/')
def name():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

'''
регистрация, чтоб только админ мог добавлять и удалять позиции из меню
подправить картинки,
сделать по красивее меню!!!!
'''
