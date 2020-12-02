import datetime
import os
from flask_login import UserMixin
from peewee import *
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('happy_trails.sqlite')

class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(BaseModel):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField()

class Post(BaseModel):
    who = ForeignKeyField(User, backref='posts')
    what = CharField()
    where = CharField()
    when = CharField()
    why = CharField()

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe = True)
    print("TABLES CREATED")
    DATABASE.close()
