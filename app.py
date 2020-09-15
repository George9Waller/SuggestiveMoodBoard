from flask import Flask, g, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap

from Forms import forms_auth, forms_site
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
    """tries to load the use matching the user id, catching the error if the user does not exist"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database via the global variable before each request"""
    g.db = models.DATABASE
    g.db.connect(reuse_if_open=True)
    # sets the global variable user to the current user
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Handles user registration"""
    form = forms_auth.RegisterFrom()
    if form.validate_on_submit():
        flash("Registration successful", "success")
        if form.usertype.data == 'Technician':
            usernum = 1
        elif form.usertype.data == 'Student':
            usernum = 2
        else:
            usernum = 0
        """created new user"""
        user = models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            usertype=usernum
        )
        # returns user to index after registration
        return redirect(url_for('index'))
    # reloads page on unsuccessful registration
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Handles user login"""
    form = forms_auth.LoginForm()
    if form.validate_on_submit():
        """tries to match the username to an existing user"""
        try:
            user = models.User.get(models.User.UserName == form.username.data)
        except models.DoesNotExist:
            flash("Email and/or password do not match", "error")
        else:
            """checks hashed password with database"""
            if check_password_hash(user.PasswordHash, form.password.data):
                login_user(user)
                flash("Login successful", "success")
                return redirect(url_for('index'))
            else:
                flash("Email and/or password do not match", "error")
    # reloads page on unsuccessful login
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """logs out user and redirects them to login"""
    logout_user()
    flash("Logout successful", "success")
    return redirect(url_for('login'))


@app.route('/add-board', methods=['GET', 'POST'])
@login_required
def new_board():
    """Handles creating a new board"""
    form = forms_site.NewBoard()
    if form.validate_on_submit():
        flash("Board Added", "success")
        models.Board.create(User=g.user.id, Name=form.name.data,
                            VenueSize=form.venuesize.data, EventDate=form.eventdate.data)
        return redirect(url_for('index'))
    # reloads page on unsuccessful form
    return render_template('add-board.html', form=form)


@app.route('/<int:boardid>')
@login_required
def board(boardid):
    """loads a board - checking if the current user is owner"""
    board = models.Board.get_board(boardid)
    if board.User == current_user:
        return render_template('board.html', board=board)
    else:
        flash("This is not your board", "error")
        return redirect(url_for('index'))


@app.route('/delete/board/<int:boardid>', methods=['GET', 'POST'])
@login_required
def delete_board(boardid):
    """delete board form, checking the board exists and the current user is its owner"""
    form = forms_site.DeleteBoardForm()
    if form.validate_on_submit():
        # checks the board exists
        try:
            models.Board.get(models.Board.id == boardid)
        except models.DoesNotExist:
            flash("Board does not exist", "error")
            return redirect(url_for('index'))
        else:
            # checks the current user owns the board
            board = models.Board.get(models.Board.id == boardid)
            if board.User != current_user:
                flash('This is not your board!', "error")
                return redirect(url_for('index'))
            else:
                flash("Board Deleted", "success")
                models.Board.delete_by_id(boardid)
                # deletes all ideas associated with the board
                models.Idea.delete().where(models.Idea.Board == models.Board.get_board(boardid))
                return redirect(url_for('index'))
        # if the form is not valid - checks if the board exists to reload the form or redirects the user to index
    else:
        try:
            board = models.Board.get(models.Board.id == boardid)
            return render_template('delete-board.html', form=form, board=board)
        except models.DoesNotExist:
            flash("Board does not exist", "error")
            return redirect(url_for('index'))


@app.route('/<int:boardid>/<int:ideaid>', methods=['GET', 'POST'])
@login_required
def edit_idea(boardid, ideaid):
    """edit an existing idea"""
    form = forms_site.IdeaForm()


@app.route('/<int:boardid>/new-idea', methods=['GET', 'POST'])
@login_required
def new_idea(boardid):
    """create new idea"""
    form = forms_site.IdeaForm()
    print("Requested idea")
    if form.validate_on_submit():
        flash("Idea Created", "success")
        models.Idea.create(Name=form.name.data.strip(), Content=form.content.data.strip(),
                           Board=models.Board.get_board(boardid))
        return redirect('/{}'.format(boardid))
    # reloads page on unsuccessful form
    return render_template('idea.html', form=form)


@app.route('/')
@login_required
def index():
    """index view showing the user their board(s)"""
    boards = models.User.get_boards(g.user.id)
    return render_template('index.html', boards=boards)


if __name__ == 'app':
    models.initialise()
    try:
        # creates a user for testing
        models.User.create_user(
            username="GeorgeWaller",
            email="george.waller3@gmail.com",
            password="flask",
            usertype=0
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
