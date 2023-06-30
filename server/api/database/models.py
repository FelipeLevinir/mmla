from .db import db
from datetime import datetime

class Experiment(db.Document):
    name = db.StringField(required=True)
    code = db.StringField(required=True)
    description = db.StringField()
    date = db.DateTimeField(default=datetime.utcnow)

class File(db.EmbeddedDocument):
    filename = db.StringField(required=True)
    type = db.StringField( required=True)
    length = db.IntField(min_value=0)
    frames = db.IntField(min_value=0)
    rate = db.IntField(min_value=0)
    fps = db.IntField(min_value=0)

class Activity(db.Document):
    name = db.StringField(required=True, unique=True)
    date = db.DateTimeField()
    num_participants = db.IntField(min_value=0)
    comment = db.StringField()
    files = db.ListField(db.EmbeddedDocumentField(File))
    experiment = db.ReferenceField(Experiment)
    #NUMERO DE PARTICIPANTES/ FECHA DE DESARROLLO/ COMENTARIO / ### TIPO DE CAMARA / ANGULO DE VISION 

class Analysis(db.Document):
    time = db.DateTimeField(default=datetime.now)
    id_activity = db.ReferenceField(Activity)
    start = db.IntField(min_value=0) 
    end = db.IntField(min_value=0)
    indicators = db.ListField(db.StringField())

class User(db.Document):
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    phone_numbers = db.ListField(db.StringField(max_length=20))
    is_active = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    password = db.StringField(required=True, min_length=6)
    meta = {
        'collection': 'users',
        'strict': False,
        'indexes': [
            'email',
            'phone_numbers'
        ]
    }

class MarkType(db.Document):
    name = db.StringField(required=True)
    experiment = db.ReferenceField(Experiment)
    marklevel = db.ListField(db.ReferenceField('MarkLevel'))

class MarkLevel(db.Document):
    name = db.StringField(required=True)
    value = db.StringField()
    marktype = db.ReferenceField(MarkType)

class Event(db.Document):
    start_time = db.IntField(min_value=0)
    end_time = db.IntField(min_value=0)
    activity = db.ReferenceField(Activity)

# class Mark(db.Document):
#     comment = db.StringField()
#     time_in_video = db.IntField(required=True)
#     marktype = db.ReferenceField(MarkType)
#     experiment = db.ReferenceField(Experiment)
#     event = db.ReferenceField(Event)
class Mark(db.Document):
    comment = db.StringField()
    time_in_video = db.IntField(required=True)
    mark_type = db.ListField(db.ReferenceField('MarkType'))
    experiment = db.ReferenceField(Experiment)
    event = db.ReferenceField(Event)