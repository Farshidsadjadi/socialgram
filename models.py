from mongoengine import *
import datetime
class User(Document):
    email = StringField(required=True, unique=True)
    phone = IntField(min_value=8)
    password = StringField(required=True)
    firstname = StringField (required=True)
    lastname = StringField(required=True)
    registered_time = DateTimeField(required=True, default=datetime.datetime.now)
    last_login = DateTimeField()

    @classmethod
    def userexist(cls, email):
        result_query = cls.objects(email=email)
        if len(result_query) == 0:
            return False
        else:
            return result_query[0]


    def pass_match(self, password):
        if self.password == password:
            return True
        else:
            return False



class Post(Document):
    image = StringField(required=True, unique=True)
    caption = StringField(max_length=200)
    user = ReferenceField(User)
    create_date = DateTimeField(required=True, default=datetime.datetime.now)

