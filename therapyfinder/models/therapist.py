"""
Therapistfinder - therapistfinder/models/therapist.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

# Global imports
from therapyfinder.const.therapist import CALL_NO_SUCCESS_OTHER
import peewee
import datetime

# Local imports
from therapyfinder.models import Database
from therapyfinder.models.user import User as UserModel

class Therapist(peewee.Model):

    custom_id = peewee.CharField(default=None, null=True)
    user = peewee.ForeignKeyField(UserModel)

    enabled = peewee.BooleanField(default=True)

    title = peewee.CharField()
    name = peewee.CharField()
    
    plz = peewee.CharField(max_length=10)
    street = peewee.CharField()
    city = peewee.CharField()

    phone = peewee.CharField()
    mobile = peewee.CharField()

    specialism = peewee.CharField()

    class Meta:
        database = Database.get()

class Timeslot(peewee.Model):

    therapist = peewee.ForeignKeyField(Therapist)
    
    weekday = peewee.IntegerField() # 0 -> Monday

    start_hour = peewee.IntegerField()
    start_minute = peewee.IntegerField()
    end_hour = peewee.IntegerField()
    end_minute = peewee.IntegerField()

    class Meta:
        database = Database.get()

class LogEntry(peewee.Model):

    user = peewee.ForeignKeyField(UserModel)
    therapist = peewee.ForeignKeyField(Therapist)

    time = peewee.DateTimeField(default=datetime.datetime.now)

    result = peewee.IntegerField(default=CALL_NO_SUCCESS_OTHER) # see const/therapist
    comment = peewee.TextField(default="")
    
    class Meta:
        database = Database.get()


Database.register_models(Therapist, Timeslot, LogEntry)