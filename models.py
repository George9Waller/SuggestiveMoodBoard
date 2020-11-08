from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from flask import flash
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import math
from WebColourNames import web_colour_names_lower, web_colour_names_upper

testing = False

if testing:
    """For testing use SQLite database"""
    DATABASE = SqliteDatabase('moodboard.db')
else:
    """For deployment use Postgres database"""
    try:
        try:
            import environment
            environment.create_database_environment_variables()
        except ModuleNotFoundError:
            pass
        DATABASE = PostgresqlDatabase(os.environ.get('DATABASE_ID'), user=os.environ.get('DATABASE_USER'),
                                      password=os.environ.get('DATABASE_PASSWORD'),
                                      host=os.environ.get('DATABASE_HOST'), port='5432')
    except OperationalError:
        DATABASE = SqliteDatabase('database.db')


def calculate_colour(c):
    """run the contrast calculation on a rgb component"""
    c = c / 255.0
    if c <= 0.03928:
        c = c / 12.92
    else:
        c = math.pow((c + 0.055) / 1.055, 2.4)
    return c


def convert_colour_name_to_hex(colour_in):
    """Converts a colour name to hex code from look-up dictionary"""
    try:
        if str(colour_in)[0] != '#':
            try:
                # tries to convert it from a word to hex code using 140 colours supported by browsers
                return web_colour_names_lower[str(colour_in)]
            except KeyError:
                try:
                    return web_colour_names_upper[str(colour_in)]
                except KeyError:
                    return '#ffffff'
        else:
            return '#ffffff'
    except:
        return '#ffffff'


class User(UserMixin, Model):
    """User Model"""
    id = PrimaryKeyField()
    UserName = CharField(unique=True)
    Email = CharField(unique=True)
    PasswordHash = CharField(max_length=100)
    UserType = IntegerField(default=0)

    class Meta:
        database = DATABASE
        order_by = ('UserID',)

    def get_boards(self):
        """returns all the boards with a user matching the supplied user, ordered by soonest first"""
        return Board.select().where(Board.User == self).order_by(Board.EventDate)

    def get_user_by_email(self):
        """returns user object matching given email"""
        return User.get(User.Email == self)

    def get_user_by_id(self):
        """returns user object matching id"""
        return User.get(User.id == self)

    def get_user_by_username(self):
        """returns user object matching username"""
        return User.get(User.UserName == self)

    def get_id(self):
        """returns the id for the supplied user"""
        return self.id

    def get_email(self):
        """returns the email address of teh supplied user"""
        return self.Email

    def get_username(self):
        """returns the username for the user"""
        return self.UserName

    def get_usertype(self):
        """returns the user type number"""
        return self.UserType

    def get_reset_token(self, expires_sec=3600):
        """returns reset token for password reset"""
        s = Serializer('`^=m%"(6"N*b3;"_u{3$5=]JAb7"tE!ttX/-8+!SG=*W`Y%.h8jgJ[!:bS6VLy@s=g"Jvq', expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """verifies a reset token"""
        s = Serializer('`^=m%"(6"N*b3;"_u{3$5=]JAb7"tE!ttX/-8+!SG=*W`Y%.h8jgJ[!:bS6VLy@s=g"Jvq')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.get_user_by_id(user_id)

    def set_new_password(self, new_password):
        """Updates the password for the user"""
        User.update(PasswordHash=generate_password_hash(new_password)).where(User == self).execute()
        print("updated {username}'s password to {password}".format(username=self.UserName, password=new_password))
        return

    @classmethod
    def create_user(cls, username, email, password, usertype=0):
        """class method to create new instance of user"""
        try:
            cls.create(
                UserName=username,
                Email=email,
                PasswordHash=generate_password_hash(password),
                UserType=usertype
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Board(Model):
    """Board Model"""
    id = PrimaryKeyField()
    User = ForeignKeyField(User, related_name='boards')
    Name = CharField(max_length=30)
    VenueSize = CharField(default='Small')
    EventDate = DateField(default=datetime.date.today)
    Created = DateField(default=datetime.date.today)
    publicreadonly = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('User',)

    def get_user(self):
        """returns the User object for the supplied board"""
        return self.User

    def get_id(self):
        """returns the id of the supplied board"""
        return self.id

    def get_board(self):
        """returns the board matching the supplied id"""
        return Board.get(Board.id == self)

    def get_ideas(self):
        """returns all the ideas associated with the board"""
        try:
            return Idea.select().where(Idea.Board == self)
        except DoesNotExist:
            return None

    def get_boards_by_user(self):
        """returns boards for the user of the supplied id"""
        return Board.select().join(User).where(Board.User.id == self)

    def set_publicreadonly(self, value):
        """sets the value of publicreadonly"""
        if value == 'true':
            return Board.update(publicreadonly=True).where(Board.id == self.id).execute()
        elif value == 'false':
            return Board.update(publicreadonly=False).where(Board.id == self.id).execute()
        else:
            return None

    def get_publicreadonly(self):
        """returns the value for publicreadonly"""
        return self.publicreadonly

    @staticmethod
    def create_board(user, name, venuesize='Small', eventdate=datetime.date.today):
        """class method to create a new board"""
        return Board.create(User=user, Name=name, VenueSize=venuesize, EventDate=eventdate)


class Idea(Model):
    """Idea Model"""
    id = PrimaryKeyField()
    Board = ForeignKeyField(Board, related_name='ideas')
    Name = CharField(max_length=30)
    Content = TextField()
    """tags"""
    Colour = CharField(max_length=7, default='black')

    class Meta:
        database = DATABASE
        order_by = ('Board',)

    def get_idea(self):
        """returns the idea matching the supplied id"""
        return Idea.get(Idea.id == self)

    def get_owner(self):
        """returns User who owns the idea"""
        idea = Idea.get_idea(self)
        return idea.Board.User.id

    def get_boardid(self):
        """returns the id of the board of the supplied ideaid"""
        idea = Idea.get_idea(self)
        return idea.Board.id

    def delete_by_board(self):
        """deletes Ideas where the board matches the supplied"""
        Idea.delete().where(Idea.Board == self)
        return

    def update_idea_by_id(self, name, content, colour):
        """updates the idea with a matching id"""
        # checks for colour names
        colour_out = convert_colour_name_to_hex(colour)

        Idea.update({Idea.Name: name, Idea.Content: content, Idea.Colour: colour_out}).where(Idea.id == self).execute()
        return

    def get_colour_ideas_by_board(self):
        """returns all the ideas with a colour from supplied board"""
        return Idea.select().where((Idea.Board == self) & ((Idea.Colour != 'black') & (Idea.Colour != '')))

    def get_colour(self):
        """Returns the colour attribute of supplied idea"""
        return self.Colour

    def get_ideas_by_tag(self):
        """returns all the ideas linked to the given tag"""
        return Idea.select().join(Idea_Tag).where(Idea_Tag.Tag == self)

    @staticmethod
    def filter(query, board):
        """Returns a filtered selection of ideas from the query"""
        if query == 'Colour':
            return Idea.select().where((Idea.Board == board) & ((Idea.Colour != 'black') & (Idea.Colour != '')))
        elif query == 'All':
            return Idea.select().where(Idea.Board == board)
        elif query is None:
            return Idea.select().where(Idea.Board == board)
        elif query:
            return Idea.select().join(Idea_Tag).join(Tag).where((Tag.id == query) & (Tag.Board == board))
        else:
            flash("Tag not recognised", "error")
            ideas = Idea.select().where(Idea.Board == board)
        return ideas

    @staticmethod
    def create_idea(name, board, content, colour: str):
        """method to create a new Idea"""

        # check colour value in case of word
        out_colour = convert_colour_name_to_hex(colour)

        return Idea.create(Name=name, Board=board, Content=content, Colour=out_colour)


class Tag(Model):
    id = PrimaryKeyField()
    Board = ForeignKeyField(Board, related_name='Tags')
    Name = CharField(max_length=30)
    Colour = CharField(max_length=7)
    textcolour = CharField(max_length=7)

    @staticmethod
    def gettagbyid(tagid):
        """returns the tag object matching the id"""
        return Tag.get(Tag.id == tagid)

    def get_tags_by_board(self):
        """returns tags matching the supplied board"""
        return Tag.select().where(Tag.Board == self)

    def get_tags_by_idea(self):
        """returns tag objects linked to the supplied idea"""
        return Tag.select().join(Idea_Tag).where(Idea_Tag.Idea == self)

    def get_board(self):
        """returns the board of the supplied board"""
        return self.Board

    def delete_by_object(self):
        """deletes Tag object matching supplied"""
        Tag.delete_instance(self)
        return

    class Meta:
        database = DATABASE
        order_by = ('Board',)

    @staticmethod
    def create_tag(board, name, colour):
        """method to create a new Tag"""

        # determine TextColour based on tag colour [https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color]
        # splits hex into rgb accepting both regular and shortened hex input
        rgb = [0, 0, 0]
        colour = str(colour)
        colour = str(convert_colour_name_to_hex(colour))
        if len(colour[1:]) == 6:
            r = int(colour[1:3], 16)
            g = int(colour[3:5], 16)
            b = int(colour[5:7], 16)
        elif len(colour[1:]) == 3:
            r = int((colour[1] + colour[1]), 16)
            g = int((colour[2] + colour[2]), 16)
            b = int((colour[3] + colour[3]), 16)
        else:
            r = 255
            g = 255
            b = 255

        r = calculate_colour(r)
        g = calculate_colour(g)
        b = calculate_colour(b)

        L = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
        if L > 0.179:
            text_colour = '#000000'
        else:
            text_colour = '#ffffff'

        return Tag.create(Board=board, Name=name, Colour=colour, textcolour=text_colour)


class Idea_Tag(Model):
    id = PrimaryKeyField
    Idea = ForeignKeyField(Idea, related_name='Tag linker')
    Tag = ForeignKeyField(Tag, related_name='Tag linker')

    def gettagids(self):
        """gets the tag ids for the supplied idea"""
        return Idea_Tag.select(Idea_Tag.Tag).where(Idea_Tag.Idea == self).dicts()

    def get_tag(self):
        """returns tag object for supplied Idea_Tag object"""
        return self.Tag

    def get_taglinks_by_ideaid(self):
        """returns all the Idea_Tag objects for the given ideaid"""
        return Idea_Tag.select().join(Idea).where(Idea_Tag.Idea.id == self)

    def get_taglinks_by_idea(self):
        """returns all the Idea_Tag objects for the given idea"""
        return Idea_Tag.select().join(Idea).where(Idea_Tag.Idea == self)

    def get_taglinks_by_tag(self):
        """returns all the Idea_Tag objects for the given tag"""
        return Idea_Tag.select().where(Idea_Tag.Tag == self)

    def delete_by_object(self):
        """deletes the object passed"""
        Idea_Tag.delete_instance(self)
        return

    class Meta:
        database = DATABASE
        order_by = ('Board',)

    @staticmethod
    def create_idea_tag_link(idea, tag):
        """method to create a new Idea Tag link"""
        return Idea_Tag.create(Idea=idea, Tag=tag)


def initialise():
    DATABASE.connect()
    # DATABASE.drop_tables([User, Board, Idea, Tag, Idea_Tag])
    DATABASE.create_tables([User, Board, Idea, Tag, Idea_Tag], safe=True)
    # DATABASE.execute_sql("UPDATE Board SET publicreadonly = False")
    DATABASE.close()
