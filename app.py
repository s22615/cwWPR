import datetime
from flask import (Flask, redirect, url_for, render_template, request, session)


class User:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User:{self.login}'


users = [User(id=1, login='Sebastian', password='123'), User(id=2, login='Jan', password='abc')]

app = Flask(__name__)
app.secret_key = 'ei031923ha42194hp;'


@app.route('/')
def main():
    return redirect('login')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = [x for x in users if x.login == login]
        if user and user[0].password == password:
            session['user_id'] = user[0].id
            session['login'] = login
            session['timestamp'] = datetime.datetime.now()
            return redirect(url_for('home'))
        else:
            return render_template('index.html', login=login, wrongpass='Wrong Password!')
    return render_template('index.html')


@app.route('/logout', methods=('POST',))
def logout():
    del session['login']
    del session['timestamp']
    return redirect(url_for('main'))


@app.route('/home', methods=('GET', 'POST'))
def home():
    age = datetime.datetime.now() - session['timestamp']
    if age > datetime.timedelta(seconds=30):
        return redirect(url_for('logout'))
    return render_template('home.html', name=session['login'], age=age)
