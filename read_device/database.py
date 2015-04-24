import datetime
import json

from peewee import *

db = Proxy()

def connect(dbpath):
  database = SqliteDatabase(dbpath)
  db.initialize(database)

  db.create_tables([Meter, Reading], safe=True)

def Location(what):
  if isinstance(what, list):
    return json.dumps(what)
  else:
    return json.loads(what)

class BaseModel(Model):
  class Meta:
    database = db

class Meter(BaseModel):
  name = CharField()
  location = CharField()

class Reading(BaseModel):
  meter = ForeignKeyField(Meter, related_name='readings')
  value = DoubleField()
  property = CharField()
  timestamp = DateTimeField(default=datetime.datetime.now)
