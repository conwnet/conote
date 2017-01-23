import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

def next_id():
    return '%s' % uuid.uuid1().hex

class Note(Model):
    __table__ = 'note'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(63)')
    author_id = StringField(ddl='varchar(63)')
    prev_id = StringField(ddl='varchar(63)')
    next_id = StringField(ddl='varchar(63)')
    title = StringField(ddl='varchar(255)')
    content = TextField()
    public = BooleanField()
    create_at = FloatField(default=time.time)

class User(Model):
    __table__ = 'user'

    def fill(self, username, password, email, power):
        self.username = username
        self.password = password
        self.email = email
        self.power = power

    id = StringField(primary_key=True, default=next_id, ddl='varchar(63)')
    username = StringField(ddl='varchar(127)')
    password = StringField(ddl='varchar(127)')
    email = StringField(ddl='varchar(127)')
    power = IntegerField()
    create_at = FloatField(default=time.time)

