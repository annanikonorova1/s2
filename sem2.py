import secrets

from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)
app.secret_key = secrets.token_hex()

category = [
    {"title": 'Home page', "func_name": 'index'},
    {"title": 'Button page', "func_name": 'button'},
    {"title": 'Image page', "func_name": 'image'},
    {"title": 'Upload image page', "func_name": 'image_get'},
    {"title": 'Login page', "func_name": 'login'},
    {"title": 'Send text page', "func_name": 'send'},
    {"title": 'Calculate page', "func_name": 'calc'},
    {"title": 'Check age page', "func_name": 'check_age'},
    {"title": 'Square page', "func_name": 'square'},
    {"title": 'Flash page', "func_name": 'flas'},
    {"title": 'Log page', "func_name": 'log'}
]

users = ['John', 'Olga', 'Smith']
info = {
    'John': '123',
    'Olga': 'qwerty',
    'Smith': '12345'
}


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', category=category)


@app.route('/button/', methods=['GET', 'POST'])
def button():
    if request.method == 'POST':
        return 'Hello Bob'
    return render_template('button.html')


@app.route('/image/')
def image():
    return render_template('image.html')


@app.get('/upload/')
def image_get():
    return render_template('upload.html')


@app.post('/upload/')
def image_post():
    file = request.files.get('file')
    file_name = secure_filename(file.filename)
    file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
    return f"Файл {file_name} загружен на сервер"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password == info[username]:
            return f"Hello {username}"
        else:
            return render_template('login.html')
    return render_template('login.html')












@app.route('/flas/', methods=['GET', 'POST'])
def flas():
    if request.method == 'POST':
        name = escape(request.form.get('name'))
        flash(f'Привет, {name}!', 'success')
        return redirect(url_for('flas'))
    return render_template('flas.html')


@app.route('/log/', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('index'))
    return render_template('log.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()