from google.appengine.api import users
from google.appengine.ext import ndb
from timeutils import *

class Generation(ndb.Model):
    """A main model for representing a generation."""
    name          = ndb.StringProperty(indexed=True)
    email         = ndb.StringProperty(indexed=True)
    date          = ndb.DateTimeProperty(auto_now_add=True)
    script        = ndb.StringProperty(indexed=False)
    status        = ndb.StringProperty(indexed=True)
    niter         = ndb.StringProperty(indexed=False)
    def string(self):
        content = []
        content.append("** " + self.name)
        content.append(" - name: "   + str(self.name))
        content.append(" - email: "  + str(self.email))
        content.append(" - date: "   + datedump(self.date))
        content.append(" - script: " + str(self.script))
        content.append(" - status: " + str(self.status))
        content.append(" - niter: "  + str(self.niter))
        return "\n".join(content)
    
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
    publishdescription  = ndb.StringProperty(indexed=False)
    publishcategories   = ndb.StringProperty(indexed=False)
    publishtags         = ndb.StringProperty(indexed=False)
    def string(self):
        content = []
        content.append("** " + self.name)
        content.append(" - name: "   + str(self.name))
        content.append(" - email: "  + str(self.email))
        content.append(" - date: "   + datedump(self.date))
        content.append(" - generationname: " + str(self.generationname))
        content.append(" - imageurl: " + str(self.imageurl))
        content.append(" - like: "  + str(self.like))
        content.append(" - renderstatus: "  + str(self.renderstatus))
        content.append(" - script: "  + str(self.script))
        content.append(" - renderniter: "  + str(self.renderniter))
        content.append(" - rendersize: "  + str(self.rendersize))
        content.append(" - publishstatus: "  + str(self.publishstatus))
        content.append(" - publishtitle: "  + str(self.publishtitle))
        content.append(" - publishdescription: "  + str(self.publishdescription))
        content.append(" - publishcategories: "  + str(self.publishcategories))
        content.append(" - publishtags: "  + str(self.publishtags))
        return "\n".join(content)
    

