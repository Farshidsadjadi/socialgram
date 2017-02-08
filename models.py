from mongoengine import *
import datetime
class User(Document):
    email = StringField(required=True, unique=True)
    phone = IntField(min_value=8)
    password = StringField(required=True)
    firstname = StringField (required=True)
    lastname = StringField(required=True)
    registered_time = DateTimeField(required=True, default=datetime.datetime.now)
    last_login = DateTimeField(default=datetime.datetime.now)


class Post(Document):
    image = ImageField(size=(800,600,True))
    caption = StringField(max_length=200)
    user = ReferenceField(User)
    create_date = DateTimeField(required=True, default=datetime.date.now)



