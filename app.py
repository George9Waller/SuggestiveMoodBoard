from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap
import os

from Forms import forms_auth, forms_site
import models

DEBUG = True
# HOST = '127.0.0.1'
# PORT = 5000

app = Flask(__name__)
app.secret_key = '`^=m%"(6"N*b3;"_u{3$5=]JAb7"tE!ttX/-8+!SG=*W`Y%.h8jgJ[!:bS6VLy@s=g"Jvq'
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

colour_create = "#38A67E"  # green
colour_view = "#F2F2F2"  # grey
colour_update = "#78BFB8"  # teal
colour_delete = "#F26835"  # orange


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
    return render_template('add-board.html', form=form, colour=colour_create)


@app.route('/<int:boardid>')
@login_required
def board(boardid):
    """loads a board - checking if the current user is owner + checks query string to filter ideas shown"""
    board = models.Board.get_board(boardid)
    query = request.args.get('filter')
    ideas = models.Idea.filter(models.Idea, query, board)

    if board.User == current_user:
        if query:
            return render_template('board.html', board=board, ideas=ideas, query=": {}".format(query), queryid=query)
        else:
            return render_template('board.html', board=board, ideas=ideas, query="", queryid=query)
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
                # deletes all ideas associated with the board
                models.Idea.delete().where(models.Idea.Board == models.Board.get_board(boardid))
                models.Board.delete_by_id(boardid)
                return redirect(url_for('index'))
        # if the form is not valid - checks if the board exists to reload the form or redirects the user to index
    else:
        try:
            board = models.Board.get(models.Board.id == boardid)
            return render_template('delete-board.html', form=form, board=board, colour=colour_delete)
        except models.DoesNotExist:
            flash("Board does not exist", "error")
            return redirect(url_for('index'))


@app.route('/delete/idea/<int:ideaid>', methods=['GET', 'POST'])
@login_required
def delete_idea(ideaid):
    """delete idea form, checking the idea exists and the current user is its owner"""
    form = forms_site.DeleteIdeaForm()
    if form.validate_on_submit():
        # checks the idea exists
        try:
            models.Idea.get(models.Idea.id == ideaid)
        except models.DoesNotExist:
            flash("Idea does not exist", "error")
            return redirect(url_for('index'))
        else:
            # check who owns the idea
            if models.Idea.get_owner(ideaid) == current_user.id:
                flash("Idea Deleted", "success")
                boardid = models.Idea.get_idea(ideaid).Board.id
                models.Idea.delete_by_id(ideaid)
                # Delete all tags ascociated with the idea
                """TODO"""
                return redirect('/{}'.format(boardid))
            else:
                flash("Error, this is not your idea", "error")
                return redirect(url_for('index'))
        # if the form is not valid - checks if the idea exists to reload the form or redirects the user to index
    else:
        try:
            idea = models.Idea.get(models.Idea.id == ideaid)
            return render_template('delete-idea.html', form=form, idea=idea, colour=colour_delete)
        except models.DoesNotExist:
            flash("Idea does not exist", "error")
            return redirect(url_for('index'))


@app.route('/<int:boardid>/<int:ideaid>', methods=['GET', 'POST'])
@login_required
def edit_idea(boardid, ideaid):
    """edit an existing idea"""
    # catches an invalid boardid or ideaid
    try:
        form = forms_site.IdeaForm()
        idea = models.Idea.get_idea(ideaid)

        # check current user is owner
        if models.Board.get_board(boardid).User != current_user:
            flash("This is not your data", "error")
            return redirect('/')

        # checks idea is in specified board
        if models.Idea.get_idea(ideaid).Board != models.Board.get_board(boardid):
            flash("This idea is not in the specified board", "error")
            return redirect('/')

        if form.validate_on_submit():
            flash("Idea Updated", "success")
            (models.Idea.update({models.Idea.Name: form.name.data.strip(), models.Idea.Content: form.content.data.strip(),
                                 models.Idea.Colour: form.colour.data, models.Idea.FixtureType: form.fixturetype.data,
                                 models.Idea.FixtureAngle: form.fixtureangle.data, models.Idea.Red: form.red.data.strip(),
                                 models.Idea.Green: form.green.data.strip(), models.Idea.Blue: form.blue.data.strip(),
                                 models.Idea.Yellow: form.yellow.data.strip()})
             .where(models.Idea.id == ideaid).execute())
            return redirect('/{}'.format(boardid))
        else:
            # load existing data into form
            form.name.data = idea.Name
            form.content.data = idea.Content
            form.colour.data = idea.Colour
            form.fixturetype.data = idea.FixtureType
            form.fixtureangle.data = idea.FixtureAngle
            form.red.data = idea.Red
            form.green.data = idea.Green
            form.blue.data = idea.Blue
            form.yellow.data = idea.Yellow
        # reloads page on unsuccessful form
        return render_template('idea.html', form=form, idea=idea, delete=True, colour=colour_update)
    except models.DoesNotExist:
        flash("error", "error")
        return redirect('/')


@app.route('/<int:boardid>/new-idea', methods=['GET', 'POST'])
@login_required
def new_idea(boardid):
    """create new idea"""
    # catches an invalid boardid
    try:
        form = forms_site.IdeaForm()
        print("Requested idea")
        if form.validate_on_submit():
            flash("Idea Created", "success")
            models.Idea.create(Name=form.name.data.strip(), Content=form.content.data.strip(),
                               Board=models.Board.get_board(boardid), Colour=form.colour.data,
                               FixtureType=form.fixturetype.data, FixtureAngle=form.fixtureangle.data,
                               Red=form.red.data.strip(), Green=form.green.data.strip(), Blue=form.blue.data.strip(),
                               Yellow=form.yellow.data.strip())
            return redirect('/{}'.format(boardid))
        # reloads page on unsuccessful form
        return render_template('idea.html', form=form, colour=colour_create)
    except models.DoesNotExist:
        flash("error", "error")
        return redirect('/')


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
    app.run(debug=DEBUG, port=int(os.environ.get('PORT', 5000)), use_reloader=True, host='0.0.0.0')
