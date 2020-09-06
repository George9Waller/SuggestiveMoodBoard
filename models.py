from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

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


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
