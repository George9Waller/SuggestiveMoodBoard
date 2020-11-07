from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
import random
import os

from Forms import forms_auth, forms_site
import sampleideas
import models
from suggestions import suggestions_algorithm
from WebColourNames import web_colour_names_upper
from StaticLookupDictionaries import usertype_to_num

DEBUG = True
# HOST = '127.0.0.1'
# PORT = 5000

app = Flask(__name__)
Bootstrap(app)

deploy = True


try:
    import environment
    environment.create_app_environment_variables()
except ModuleNotFoundError:
    pass


app.secret_key = os.environ.get('SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASS")
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

colour_create = "#66cca7"  # green
colour_view = "#F2F2F2"  # grey
colour_update = "#78BFB8"  # teal
colour_delete = "#F26835"  # orange


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Link', sender='"Thought Base <thoughtbasehelp@gmail.com>"', recipients=[user.get_email()])
    msg.html = render_template('ResetPassword-email.html', site_url='http://suggestivemoodboard.herokuapp.com',
                               reset_url=url_for('reset_token', token=token, _external=True))
    mail.send(msg)


def send_username_reminder(user):
    msg = Message('Username Reminder', sender='"Thought Base <thoughtbasehelp@gmail.com>"', recipients=[user.get_email()])
    msg.html = render_template('UsernameReminder-email.html', site_url='http://suggestivemoodboard.herokuapp.com',
                               username=user.get_username())
    mail.send(msg)


@login_manager.user_loader
def load_user(userid):
    """tries to load the use matching the user id, catching the error if the user does not exist"""
    try:
        return models.User.get_user_by_id(userid)
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
        flash("Registration successful, a sample board has been created for you", "success")
        try:
            usernum = usertype_to_num[form.usertype.data]
        except KeyError:
            usernum = 0
        """created new user"""
        user = models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            usertype=usernum
        )
        # Creates sample board to show the user an example of the solution
        sampleboard = models.Board.create_board(user=models.User.get_user_by_email(form.email.data),
                                                name='100 in the style of Complicité',
                                                venuesize='Small', eventdate='2020-10-08')
        sampleideas.addideas(sampleboard)
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
            user = models.User.get_user_by_username(form.username.data)
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
        models.Board.create_board(user=g.user.id, name=form.name.data,
                                  venuesize=form.venuesize.data, eventdate=form.eventdate.data)
        return redirect(url_for('index'))
    # reloads page on unsuccessful form
    return render_template('add-board.html', form=form, colour=colour_create)


@app.route('/<int:boardid>')
@login_required
def board(boardid):
    """loads a board - checking if the current user is owner + checks query string to filter ideas shown"""
    board = models.Board.get_board(boardid)
    query = request.args.get('filter')
    ideas = models.Idea.filter(query, board)
    tags = models.Tag.get_tags_by_board(board)

    for idea in ideas:
        idea.tags = models.Tag.get_tags_by_idea(idea)

    if board.User == current_user or current_user.get_usertype() == 99:
        if query:
            return render_template('board.html', board=board, ideas=ideas, query=": {}".format(query), queryid=query,
                                   tags=tags, models=models)
        else:
            return render_template('board.html', board=board, ideas=ideas, query="", queryid=query, tags=tags)
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
            board = models.Board.get_board(boardid)
            if board.get_user() == current_user or current_user.get_usertype() == 99:
                flash("Board Deleted", "success")
                # deletes all ideas associated with the board
                models.Idea.delete_by_board(models.Board.get_board(boardid))
                models.Board.delete_by_id(boardid)
                return redirect(url_for('index'))
            else:
                flash('This is not your board!', "error")
                return redirect(url_for('index'))
        # if the form is not valid - checks if the board exists to reload the form or redirects the user to index
    else:
        try:
            board = models.Board.get_board(boardid)
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
            models.Idea.get_idea(ideaid)
        except models.DoesNotExist:
            flash("Idea does not exist", "error")
            return redirect(url_for('index'))
        else:
            # check who owns the idea
            if models.Idea.get_owner(ideaid) == current_user.id or current_user.get_usertype() == 99:
                flash("Idea Deleted", "success")
                boardid = models.Idea.get_boardid(ideaid)

                # Delete all tags associated with the idea
                taglinks = models.Idea_Tag.get_taglinks_by_ideaid(ideaid)
                for tag in taglinks:
                    models.Idea_Tag.delete_by_object(tag)

                # delete the idea
                models.Idea.delete_by_id(ideaid)
                return redirect('/{}'.format(boardid))
            else:
                flash("Error, this is not your idea", "error")
                return redirect(url_for('index'))
        # if the form is not valid - checks if the idea exists to reload the form or redirects the user to index
    else:
        try:
            idea = models.Idea.get_idea(ideaid)
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
        board = models.Board.get_board(boardid)
        tags = models.Tag.get_tags_by_board(board)
        form = forms_site.IdeaForm()
        form.addtotag.choices = [(tag.id, tag.Name) for tag in tags]
        idea = models.Idea.get_idea(ideaid)

        # check current user is owner
        if models.Board.get_board(boardid).get_user() != current_user:
            if current_user.get_usertype() == 99:
                pass
            else:
                flash("This is not your data", "error")
                return redirect('/')

        # checks idea is in specified board
        if models.Idea.get_idea(ideaid).Board != models.Board.get_board(boardid):
            flash("This idea is not in the specified board", "error")
            return redirect('/')

        if form.validate_on_submit():
            flash("Idea Updated", "success")
            models.Idea.update_idea_by_id(ideaid, name=form.name.data.strip(), content=form.content.data.strip(),
                                          colour=form.colour.data)

            # delete all links for idea
            for todelete in models.Idea_Tag.get_taglinks_by_idea(idea):
                models.Idea_Tag.delete_by_object(todelete)

            # create all links from selection data
            for tagid in form.addtotag.data:
                models.Idea_Tag.create_idea_tag_link(idea=idea, tag=models.Tag.gettagbyid(tagid))

            return redirect('/{}'.format(boardid))
        else:
            # load existing data into form
            links = models.Idea_Tag.gettagids(idea)
            links = list(links)
            # use list comprehension to convert the list of dictionaries to a list of the values
            links = [l['Tag'] for l in links]
            # mapping the list of int to strings
            linkstr = []
            for link in links:
                linkstr.append(str(link))
            form.name.data = idea.Name
            form.content.data = idea.Content
            form.colour.data = idea.Colour
            form.addtotag.data = linkstr
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
        board = models.Board.get_board(boardid)
        tags = models.Tag.get_tags_by_board(board)
        form.addtotag.choices = [(tag.id, tag.Name) for tag in tags]

        # catches user not owning board
        if board.User != current_user:
            if current_user.get_usertype() == 99:
                pass
            else:
                flash("This is not your data", "error")
                return redirect(url_for('index'))

        if form.validate_on_submit():
            flash("Idea Created", "success")
            models.Idea.create_idea(name=form.name.data.strip(), content=form.content.data.strip(),
                                    board=models.Board.get_board(boardid), colour=form.colour.data)
            return redirect('/{}'.format(boardid))
        else:
            # reloads page on unsuccessful form
            form.addtotag.data = []

            # checks for query for colour
            query = request.args.get('colour')
            if query and len(query) == 6:
                query = '#' + query
                form.colour.data = query
            return render_template('idea.html', form=form, colour=colour_create)
    except models.DoesNotExist:
        flash("error", "error")
        return redirect('/')


@app.route('/<int:boardid>/add-tag', methods=['GET', 'POST'])
@login_required
def add_tag(boardid):
    """Add tag to a board"""
    # catches invalid board id
    try:
        form = forms_site.AddTagForm()
        if form.validate_on_submit():
            flash("Tag added", "success")
            models.Tag.create_tag(board=models.Board.get_board(boardid), name=form.name.data.strip(),
                                  colour=form.colour.data)
            return redirect('/{}'.format(boardid))
        # reloads form on unsuccessful attempt
        # checks current user owns board
        board = models.Board.get_board(boardid)
        if board.get_user() == current_user or current_user.get_usertype() == 99:
            # fill random colour from dictionary
            colour_name, colour_code = random.choice(list(web_colour_names_upper.items()))
            form.colour.data = colour_code
            return render_template('tag.html', form=form, colour=colour_create)
        else:
            flash("This is not your board", "error")
            return redirect(url_for('index'))
    except models.DoesNotExist:
        flash("error", "error")
        return redirect('/')


@app.route('/<int:boardid>/delete-tag', methods=['GET', 'POST'])
@login_required
def delete_tag(boardid):
    """Deletes tag checking it belongs to a board the current user owns"""
    form = forms_site.DeleteTagForm()
    if form.validate_on_submit():
        # checks the tag exists
        try:
            tag = models.Tag.gettagbyid(form.selectTag.data)
        except models.DoesNotExist:
            flash("Tag does not exist", "error")
            return redirect(url_for('index'))
        else:
            # checks if the tag is on a board owned by the user
            for board in models.Board.get_boards_by_user(current_user.id):
                if tag.get_board() == board or current_user.get_usertype() == 99:
                    flash("Tag Deleted", "success")
                    boardid = tag.get_board().get_id()

                    # delete all links
                    for todelete in models.Idea_Tag.get_taglinks_by_tag(tag):
                        models.Idea_Tag.delete_instance(todelete)

                    # delete the tag
                    models.Tag.delete_by_object(tag)

                    return redirect('/{}'.format(boardid))

            flash("This is not your tag", "error")
            return redirect(url_for('index'))
    else:
        try:
            # get choices
            board = models.Board.get_board(boardid)

            """Check current user owns board"""
            if board.get_user() == current_user or current_user.get_usertype() == 99:
                choices = models.Tag.get_tags_by_board(board)
                form.selectTag.choices = [(tag.id, tag.Name) for tag in choices]
                return render_template('delete-tag.html', form=form, board=board, colour=colour_delete)
            else:
                flash("This is not your board", "error")
                return redirect(url_for('index'))
        except models.DoesNotExist:
            flash("Error", "error")
            return redirect(url_for('index'))


@app.route('/<int:boardid>/suggestions', methods=['GET'])
@login_required
def suggestions(boardid):
    board = models.Board.get_board(boardid)
    colours = suggestions_algorithm(board)
    return render_template('suggestions.html', colours=colours, board=board)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('A user is already logged in', "error")
        return redirect(url_for('index'))
    form = forms_auth.RequestPasswordResetForm()
    if form.validate_on_submit():
        user = models.User.get_user_by_email(form.email.data)
        send_reset_email(user)
        flash('Sent password reset email - Please check your spam if you do not receive an email from: '
              'thoughtbasehelp@gmail.com', "success")
        return redirect(url_for('login'))
    return render_template('RequestResetPassword.html', form=form, title='Request Reset Email', submit='Request Email')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('A user is already logged in', "error")
        return redirect(url_for('index'))
    user = models.User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired', "error")
        return redirect(url_for('reset_request'))
    form = forms_auth.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_new_password(form.password.data)
        flash('Your password has been updated', "success")
        return redirect(url_for('login'))
    return render_template('RequestResetPassword.html', form=form, title='Set New Password', submit='Set Password')


@app.route('/request-username', methods=['GET', 'POST'])
def request_username():
    if current_user.is_authenticated:
        flash('A user is already logged in', "error")
        return redirect(url_for('index'))
    form = forms_auth.RequestPasswordResetForm()
    if form.validate_on_submit():
        user = models.User.get_user_by_email(form.email.data)
        send_username_reminder(user)
        flash('Sent email with your username - Please check your spam if you do not recieve an email from: '
              'thoughtbasehelp@gmail.com', 'success')
        return redirect(url_for('login'))
    return render_template('RequestResetPassword.html', form=form, title='Request Username Reminder',
                           submit='Send Reminder')


@app.route('/')
@login_required
def index():
    """index view showing the user their board(s)"""
    models.User.update(UserType=99).where(models.User.UserName == 'admin').execute()
    if current_user.get_usertype() == 99:
        boards = models.Board.select()
        return render_template('index.html', boards=boards, admin=True, models=models)
    boards = models.User.get_boards(g.user.id)
    return render_template('index.html', boards=boards)


if __name__ == 'app':
    models.initialise()
    try:
        # creates a user for testing
        models.User.create_user(
            username="admin",
            email="thoughtbasehelp@gmail.com",
            password=os.environ.get('ADMIN_PASS'),
            usertype=99
        )
        print('created admin user')
    except ValueError:
        pass

    # different host for web server
    if os.uname().nodename == 'Georges-MacBook-Pro-2.local':
        app.run(debug=DEBUG, port=int(os.environ.get('PORT', 5000)), use_reloader=True, host='127.0.0.1')
    else:
        app.run(debug=DEBUG, port=int(os.environ.get('PORT', 5000)), use_reloader=True, host='0.0.0.0')
