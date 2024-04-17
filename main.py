from flask import Flask, render_template
from data import form
from flask_login import LoginManager
import datetime

app = Flask(__name__)

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = form.Form()
    if form1.validate_on_submit():
        pass
    return render_template('base.html', form=form1)


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/basket')
def basket():
    return render_template('basket.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
