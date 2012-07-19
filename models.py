from google.appengine.ext import db

class BotResults(db.Model):
    testday = db.StringProperty(required=True)
    greetedName = db.StringListProperty()
    greetedNumber = db.IntegerProperty()
    firebotBugs = db.StringListProperty()
    usersTalks = db.StringListProperty()

class Speakers(db.Model):
    botresults = db.ReferenceProperty()
    speaker = db.StringProperty()
    spoke = db.IntegerProperty()
