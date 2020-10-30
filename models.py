from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from flask import flash
import datetime

testing = False

if testing:
    """For testing use SQLite database"""
    DATABASE = SqliteDatabase('moodboard.db')
else:
    """For deployment use Postgres database"""
    try:
        DATABASE = PostgresqlDatabase('d5o38mub306f1k', user='gankiyhoomxwod',
                                  password='db71fb788e4548b27ff125a1d74531a46e863c384cf98aa687d124470dfc4266',
                                  host='ec2-54-228-209-117.eu-west-1.compute.amazonaws.com', port='5432')
    except OperationalError:
        DATABASE = SqliteDatabase('database.db')


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
        return User.select().where(User.Email == self)

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

    class Meta:
        database = DATABASE
        order_by = ('User',)

    def get_board(self):
        """returns the board matching the supplied id"""
        return Board.get(Board.id == self)

    def get_ideas(self):
        """returns all the ideas associated with the board"""
        try:
            return Idea.select().where(Idea.Board == self)
        except DoesNotExist:
            return None

    @classmethod
    def create_board(cls, user, name, venuesize='Small', eventdate=datetime.date.today):
        """class method to create a new board"""
        try:
            cls.create(
                User=user,
                Name=name,
                VenueSize=venuesize,
                EventDate=eventdate
            )
        except IntegrityError:
            raise ValueError('Invalid details')


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
        """returns the id of the board it is on"""
        idea = Idea.get_idea(self)
        return idea.Board.id

    def filter(self, query, board):
        """Returns a filtered selection of ideas from the query"""
        if query == 'Colour':
            return Idea.select().where((Idea.Board == board) & ((Idea.Colour != 'black') & (Idea.Colour != '')))
        elif query == 'All':
            return Idea.select().where(Idea.Board == board)
        elif query is None:
            return Idea.select().where(Idea.Board == board)
        elif query:
            print('run custom query')
            return Idea.select().join(Idea_Tag).join(Tag).where(Tag.Name == query)
        else:
            flash("Tag not recognised", "error")
            ideas = Idea.select().where(Idea.Board == board)
        return ideas


class Tag(Model):
    id = PrimaryKeyField()
    Board = ForeignKeyField(Board, related_name='Tags')
    Name = CharField(max_length=30)
    Colour = CharField(max_length=7)

    def gettagbyid(self):
        """returns the tag object matching the id"""
        return Tag.get(Tag.id == self)

    class Meta:
        database = DATABASE
        order_by = ('Board',)


class Idea_Tag(Model):
    id = PrimaryKeyField
    Idea = ForeignKeyField(Idea, related_name='Tag linker')
    Tag = ForeignKeyField(Tag, related_name='Tag linker')

    def gettagids(self):
        """gets the tag ids for the supplied idea"""
        return Idea_Tag.select(Idea_Tag.Tag).where(Idea_Tag.Idea == self).dicts()

    class Meta:
        database = DATABASE
        order_by = ('Board',)


def initialise():
    DATABASE.connect()
    # DATABASE.drop_tables([User, Board, Idea, Tag, Idea_Tag])
    DATABASE.create_tables([User, Board, Idea, Tag, Idea_Tag], safe=True)
    DATABASE.close()
