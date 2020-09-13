from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime

DATABASE = SqliteDatabase('moodboard.db')


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
        return Board.select().where(Board.User == self).order_by(Board.EventDate)

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
        return Board.get(Board.id == self)

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


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Board], safe=True)
    DATABASE.close()
