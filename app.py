from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap

from Forms import forms_auth
import models

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

app = Flask(__name__)
app.secret_key = '`^=m%"(6"N*b3;"_u{3$5=]JAb7"tE!ttX/-8+!SG=*W`Y%.h8jgJ[!:bS6VLy@s=g"Jvq'
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    """Close database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms_auth.RegisterFrom()
    if form.validate_on_submit():
        flash("Registration successful", "success")
        if form.usertype.data == 'Technician':
            usernum = 1
        elif form.usertype.data == 'Student':
            usernum = 2
        else:
            usernum = 0
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            usertype=usernum
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms_auth.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.UserName == form.username.data)
        except models.DoesNotExist:
            flash("Email and/or password do not match", "error")
        else:
            if check_password_hash(user.PasswordHash, form.password.data):
                login_user(user)
                flash("Login successful", "success")
                return redirect(url_for('index'))
            else:
                flash("Email and/or password do not match", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successful", "success")
    return redirect(url_for('index'))


@app.route('/')
def index():
    return 'Hello World! Welcome'


if __name__ == 'app':
    models.initialise()
    try:
        models.User.create_user(
            username="GeorgeWaller",
            email="george.waller3@gmail.com",
            password="flask",
            usertype=0
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
