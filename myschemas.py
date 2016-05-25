from google.appengine.api import users
from google.appengine.ext import ndb

#class DictModel(ndb.Model):
#    def to_dict(self):
#       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class Generation(ndb.Model):
    """A main model for representing a generation."""
    name          = ndb.StringProperty(indexed=True)
    email         = ndb.StringProperty(indexed=True)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    script        = ndb.StringProperty(indexed=False)
    status        = ndb.StringProperty(indexed=True)
    niter         = ndb.StringProperty(indexed=False)

class Genresult(ndb.Model):
    """A main model for representing a gen result."""
    name           = ndb.StringProperty(indexed=True)
    email          = ndb.StringProperty(indexed=True)
    date           = ndb.DateTimeProperty(auto_now_add=True)
    generationname = ndb.StringProperty(indexed=True)
    imageurl       = ndb.StringProperty(indexed=False)
    # scriptname     = ndb.StringProperty(indexed=False)
    like           = ndb.StringProperty(indexed=True)
    renderstatus   = ndb.StringProperty(indexed=True)
    script         = ndb.StringProperty(indexed=False)
    renderniter    = ndb.StringProperty(indexed=False)
    rendersize     = ndb.StringProperty(indexed=False)
    publishstatus  = ndb.StringProperty(indexed=True)
    publishtitle   = ndb.StringProperty(indexed=False)
    publishdescription   = ndb.StringProperty(indexed=False)
    publishcategories   = ndb.StringProperty(indexed=False)
    publishtags   = ndb.StringProperty(indexed=False)
    

