import mongoengine as me
import datetime as dt


class User(me.Document):
    username = me.StringField(required = True, max_length = 32)
    password = me.StringField(required = True, max_length = 16)
    wellness = me.ListField(required = False)
    notes = me.ListField(required = False)
    concerns = me.ListField(required = False)
    date_created = me.DateTimeField(required = True, default = dt.datetime.now())

    def update_wellness(self, wellness):
        self.wellness.append(wellness)

    def update_notes(self, notes):
        self.notes.append(notes)

    def update_concerns(self, concerns):
        self.concerns.append(concerns)


class Wellness(me.EmbeddedDocument):
    rating = me.IntField(required = True)
    date_entered = me.DateTimeField(required = True, default = dt.datetime.now())


class Note(me.EmbeddedDocument):
    text = me.StringField(required = True)


class Concern(me.EmbeddedDocument):
    text = me.StringField(required = True)