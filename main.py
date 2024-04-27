from flask import Flask, render_template, redirect, url_for, flash, abort
from data import session
from data import users
import datetime
import flask_login
from data.positions import Position
from data.baskets import Basket
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.position import RegisterForm, LoginForm, PositionForm

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'my_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
session.global_init("db/users.db")
ADMIN = "admin"


@login_manager.user_loader
def load_user(user_id):
    db_sess = session.create_session()
    return db_sess.query(users.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        user = db_sess.query(users.User).filter(users.User.email == form.email.data).first()
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
        if db_sess.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
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
    db_sess = session.create_session()
    position1 = db_sess.query(Position)
    return render_template('menu.html', position=position1, admin=ADMIN)


@app.route('/')
def main():
    return render_template('base.html', title='Меню', admin=ADMIN)


@app.route('/basket')
def basket():
    db_sess = session.create_session()
    baskets = db_sess.query(Basket)
    summ = sum(int(b.price) for b in baskets)
    return render_template('basket.html', title='Корзина', baskets=baskets, summ=summ)


@app.route('/basket/<int:id>', methods=['GET', 'POST'])
def basket_add(id):
    db_sess = session.create_session()
    basket1 = db_sess.query(Position).filter(Position.id == id).first()
    userid = int(flask_login.current_user.id)
    if basket1:
        basket_1 = Basket(
            name=basket1.name,
            price=basket1.price,
            user_id=userid
        )

        db_sess.add(basket_1)
        db_sess.commit()
    if basket1.about == "Завтраки":
        return redirect('/breakfast')

    if basket1.about == "Напитки":
        return redirect('/drink')


@app.route('/position', methods=['GET', 'POST'])
def position():
    form = PositionForm()
    if form.validate_on_submit():
        db_sess = session.create_session()
        if db_sess.query(Position).filter(Position.name == form.name.data).first():
            return render_template('position.html', title='давай поедим',
                                   form=form,
                                   message="Такая позиция уже есть")
        if db_sess.query(Position).filter("0" >= form.price.data).first():
            return render_template('position.html', title='давай поедим',
                                   form=form,
                                   message="ЦЕНА НЕ МОЖЕТ БЫТЬ ОТРИЦАТЕЛЬНОЙ")
        if db_sess.query(Position).filter(form.about.data != "Завтраки", form.about.data != "Напитки").first():
            return render_template('position.html', title='давай поедим',
                                   form=form,
                                   message="ВЫ ВВЕЛИ НЕ ТУ КАТЕГОРИЮ. КАТЕГОРИИ ВСЕГО 2(напитки и завтраки)")

        position_1 = Position(
            name=form.name.data,
            price=form.price.data,
            img=form.img.data,
            about=form.about.data
        )
        db_sess.add(position_1)
        db_sess.commit()

        return redirect('/menu')
    return render_template('position.html', title='Добавление блюда', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/position_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def position_delete(id):
    db_sess = session.create_session()
    position = db_sess.query(Position).filter(Position.id == id).first()
    if position:
        db_sess.delete(position)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/menu')


@app.route('/position_hide/<int:id>', methods=['GET', 'POST'])
@login_required
def position_hide(id):
    db_sess = session.create_session()
    position1 = db_sess.query(Position).filter(Position.id == id).first()
    if position1.active:
        position1.active = not position1.active
        db_sess.commit()
    else:
        position1.active = not position1.active
        db_sess.commit()
    return redirect('/menu')


@app.route('/to_pay')
@login_required
def to_pay():
    db_sess = session.create_session()
    for basket1 in db_sess.query(Basket).all():
        db_sess.delete(basket1)
        db_sess.commit()

    return redirect('/')


@app.route('/drink')
@login_required
def drink():
    db_sess = session.create_session()
    position1 = db_sess.query(Position)

    return render_template('drink.html', position=position1, admin=ADMIN)


@app.route('/breakfast')
@login_required
def breakfast():
    db_sess = session.create_session()
    position1 = db_sess.query(Position)

    return render_template('breakfast.html', position=position1, admin=ADMIN)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
