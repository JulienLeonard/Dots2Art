from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from generationtemplates    import *
from mydicts          import *
from myschemas        import *
from modelutils       import *
from htmlutils        import *
from utils            import *
from timeutils        import *

def generationhandlers():
    return [('/listgenerations',       ListGenerations),
            ('/mylistgenerations/(.*)',MyListGenerations),
            ('/addgeneration',         AddGeneration),
            ('/doaddgeneration',       DoAddGeneration),
            ('/mydoaddgeneration/(.*)',MyDoAddGeneration),
            ('/deletegeneration/(.*)', DeleteGeneration),
            ('/startgeneration/(.*)',  DoStartGeneration),
            ('/stopgeneration/(.*)',   DoStopGeneration),
            ('/viewgeneration/(.*)',   ViewGeneration),
            ('/viewgenerationresults/(.*)',   ViewGenerationResults),
            ('/listgenresultspage/(.*)/(.*)',ViewGenerationResultsPage),
            ('/generationclearresults/(.*)',ClearGenerationResults)]

def addgeneration(request,name,script,niter,email):
    if email:
        dict_name = request.request.get('dict_name', USERDICT)
        ogeneration = Generation(parent=dict_key(dict_name))
        ogeneration.name        = name
        ogeneration.script      = script
        ogeneration.status      = "SLEEP"
        ogeneration.niter       = niter
        ogeneration.email       = email
        ogeneration.put()
    return ogeneration
                
    
# [START ListGeneration]
class ListGenerations(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        user = users.get_current_user()
        if user:
            rows = [[generation.name,generation.script,generation.niter,generation.status,buttonformget("/viewgeneration/" + generation.key.urlsafe(),"View"), buttonformget("/listgenresultspage/" + generation.key.urlsafe() + "/0","Results"),buttonformpost("/deletegeneration/" + generation.key.urlsafe(),"Del"), buttonformpost("/startgeneration/" + generation.key.urlsafe(),"Start"),buttonformpost("/stopgeneration/" + generation.key.urlsafe(),"Stop")] for generation in getallgenerations(self,user.email())]
            content = htmltable(htmlrows(rows))
            self.response.write(LIST_GENERATION_TEMPLATE % content)
        else:
            self.response.write('You must login')

        self.response.write('</body></html>')
# [END ListGeneration]


# [START MyListGeneration]
class MyListGenerations(webapp2.RequestHandler):
    def get(self,email):
        content = [",".join([generation.name,generation.script,generation.niter,generation.status]) for generation in getallgenerations(self,email)]
        self.response.write(";".join(content))

# [END MyListGeneration]


# [START AddGeneration]
class AddGeneration(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user == None:
            content = ADD_GENERATION_TEMPLATE
        else:
            content = 'Sorry, you must login to access this page'
        self.response.write(htmlbody(content))
# [END AddGeneration]

# [START DoAddGeneration]
class DoAddGeneration(webapp2.RequestHandler):
    def post(self):
        generationname      = self.request.get('generationname')
        generationscript    = self.request.get('generationscript')
        generationniter     = self.request.get('generationniter')
        generation = addgeneration(self,generationname,generationscript,generationniter,users.get_current_user().email())
        self.redirect("/listgenerations")
# [END DoAddChiChar]

# [START DoAddGeneration]
class MyDoAddGeneration(webapp2.RequestHandler):
    def post(self,email):
        generationname      = self.request.get('generationname')
        generationscript    = self.request.get('generationscript')
        generationniter     = self.request.get('generationniter')
        generation = addgeneration(self,generationname,generationscript,generationniter,email)
        self.redirect("/listgenerations")
# [END DoAddChiChar]

# [START DoStartGeneration]
class DoStartGeneration(webapp2.RequestHandler):
    def post(self,generationid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()
            generation.status = "TODO"
            generation.put()

        self.redirect("/listgenerations")
# [END DoAddChiChar]

# [START DoStartGeneration]
class DoStopGeneration(webapp2.RequestHandler):
    def post(self,generationid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()
            generation.status = "SLEEP"
            generation.put()

        self.redirect("/listgenerations")
# [END DoStopGeneration]



def deletegeneration(request,generationid):
    generation_key = ndb.Key(urlsafe=generationid)
    generation     = generation_key.get()
    generation.key.delete()
    

# [START DeleteGeneration]
class DeleteGeneration(webapp2.RequestHandler):
    def post(self,generationid):
        deletegeneration(self,generationid)
        self.redirect("/listgenerations")

# [END DeleteGeneration]


# [START ViewGeneration]
class ViewGeneration(webapp2.RequestHandler):
    def get(self,generationid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()

            content.append(html("h1","Description"))
            content.append(htmltable( htmlrows( [ ["Name", generation.name],["Script", generation.script],["Niter", generation.niter]])))
            content.append(html("h1","Results"))
            # content.append(htmltable(htmlrows( [ [routine.name, routine.description, routine.status, date2string(utc2local(routine.date)), buttonformget("/viewroutine/" + routine.key.urlsafe(),"+"), buttonformpost("/deleteroutine/" + routine.key.urlsafe(),"Del")] for genresult in getgenresults(generation.name,user.email()) ] ) ) )
            content.append("<hr>")
            # content.append(htmltable(htmlrow( [buttonformget("/addroutine/" + generation.key.urlsafe(),"Add Routine"), buttonformget("/listgenerations","List"), buttonformget("/","Home")])))

        content = htmlcenter(content)
        writehtmlresponse(self,content)

# [START ViewGeneration]
class ViewGenerationResults(webapp2.RequestHandler):
    def get(self,generationid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()
            results = [result for result in getgenresults(generation.name,user.email())]

            content.append(html("h1","Description"))
            content.append(htmltable( htmlrows( [ ["Name", generation.name],["Script", generation.script],["Niter", generation.niter],["Nresults", str(len(results))]])))
            content.append(html("h1","Results"))
            content.append(htmltable(htmlrow( [buttonformpost("/generationclearresults/" + generation.key.urlsafe(),"Clear Results")] )))
            content.append(htmltable(htmlrows( [ [htmllink("/viewgenresult/" + genresult.key.urlsafe(),htmlimage(thumbnailurl(genresult))) for genresult in genresult5] for genresult5 in lsplit(results[:9],3) ] ) ) )
            content.append(htmltable(htmlrow( [buttonformget("/listgenresultspage/" + generation.key.urlsafe() + "/1","Next"), buttonformget("/","Home")])))
            content.append("<hr>")
            
            
        content = htmlcenter(content)
        writehtmlresponse(self,content)


# [START ViewGeneration]
class ViewGenerationResultsPage(webapp2.RequestHandler):
    def get(self,generationid,page):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()
            # results = [result for result in getgenresults(generation.name,user.email())]
            ipage   = int(page)
            query = getgenresults(generation.name,user.email())
            countresult = query.count()
            # results     = [result for result in query.fetch(offset=ipage*9,limit=(ipage+1)*9)]
            results     = [result for result in query.fetch(9,offset=ipage*9)]

            content.append(html("h1","Description"))
            content.append(htmltable( htmlrows( [ ["Name", generation.name],["Script", generation.script],["Niter", generation.niter],["Nresults", str(countresult)]])))
            content.append(html("h1","Results"))
            content.append(htmltable(htmlrow( [buttonformpost("/generationclearresults/" + generation.key.urlsafe(),"Clear Results")] )))
            content.append("Results page indices: " + str(ipage*9) + " -> " + str((ipage+1)*9))
            content.append(htmltable(htmlrows( [ [htmllink("/viewgenresult/" + genresult.key.urlsafe(),htmlimage(thumbnailurl(genresult))) for genresult in genresult5] for genresult5 in lsplit(results,3) ] ) ) )
            content.append("<hr>")
            if ipage == 0:
                content.append(htmltable(htmlrow( [buttonformget("/listgenresultspage/" + generation.key.urlsafe() + "/1","Next"), buttonformget("/","Home")])))
            else:
                content.append(htmltable(htmlrow( [buttonformget("/listgenresultspage/" + generation.key.urlsafe() + "/" + str(int(page)-1),"Prev"), buttonformget("/listgenresultspage/" + generation.key.urlsafe() + "/" + str(int(page)+1),"Next"),buttonformget("/","Home")])))

        content = htmlcenter(content)
        writehtmlresponse(self,content)

class ClearGenerationResults(webapp2.RequestHandler):
    def post(self,generationid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            generation_key = ndb.Key(urlsafe=generationid)
            generation = generation_key.get()
            results = [result for result in getgenresults(generation.name,user.email())]

            for result in results:
                if result.like == "No":
                    result.key.delete()
        self.redirect("/viewgenerationresults/" + generationid)
