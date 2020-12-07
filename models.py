import datetime
import os
from flask_login import UserMixin
from peewee import *
from playhouse.db_url import connect

# if 'ON_HEROKU' in os.environ:
#     DATABASE = connect(os.environ.get('DATABASE_URL'))
# else:
DATABASE = SqliteDatabase('happy_trails.sqlite')

class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(BaseModel, UserMixin):
    email = CharField(unique = True)
    password = CharField()
    photo = CharField(default='https://spee.ch/0/bcfdcd31-c004-42ed-a6f0-3d9cd67f134e.jpg')
    username = CharField(unique = True)

class Post(BaseModel):
    activity = CharField()
    description = CharField()
    location = CharField()
    time = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref = 'posts')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe = True)
    print("TABLES CREATED")
    DATABASE.close()
