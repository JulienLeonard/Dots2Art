from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

from genresulttemplates    import *
from mydicts          import *
from myschemas        import *
from modelutils       import *
from htmlutils        import *
from utils            import *
from timeutils        import *

def genresulthandlers():
    return [('/listgenresults',              ListGenresults),
            ('/listgenresultspageattr/(.*)', ListGenresultsPageAttr),
            ('/mylistgenresults/(.*)',       MyListGenresults),
            ('/addgenresult',                AddGenresult),
            ('/doaddgenresult',              DoAddGenresult),
            ('/mydoaddgenresult/(.*)',       MyDoAddGenresult),
            ('/deletegenresult/(.*)',        DeleteGenresult),
            ('/viewgenresult/(.*)',          ViewGenresult),
            ('/likegenresult/(.*)/(.*)',     LikeGenresult),
            ('/rendergenresult/(.*)/(.*)',   RenderGenresult),
            ('/dorendergenresult/(.*)',      DoRenderGenresult),
            ('/mydorendergenresultend/(.*)', MyDoRenderGenresultEnd),
            ('/publishgenresult/(.*)/(.*)',  PublishGenresult),
            ('/dopublishgenresult/(.*)',     DoPublishGenresult),
            ('/mydopublishgenresultend/(.*)',MyDoPublishGenresultEnd)]

def addgenresult(request,name,generationname,imageurl,script,email):
    if email:
        dict_name = request.request.get('dict_name', USERDICT)
        ogenresult = Genresult(parent=dict_key(dict_name))
        ogenresult.name           = name
        ogenresult.email          = email
        ogenresult.generationname = generationname
        ogenresult.imageurl       = imageurl
        ogenresult.like           = "No"
        ogenresult.renderstatus   = "MAYBE"
        ogenresult.publishstatus  = "MAYBE"
        ogenresult.publishtitle   = "TOTO"
        ogenresult.script         = script
        ogenresult.put()
    return ogenresult

def addrenderresult(request,genresultname,generationname,niter):
    user = users.get_current_user()
    if user:
        dict_name = request.request.get('dict_name', USERDICT)
        renderresult = Renderresult(parent=dict_key(dict_name))
        renderresult.genresultname  = genresultname
        renderresult.generationname = generationname
        renderresult.niter          = niter
        renderresult.put()
    return renderresult


    
# [START ListGenresult]
class ListGenresults(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')

        user = users.get_current_user()
        if user:
            rows = [[genresult.name,genresult.generationname,genresult.imageurl,genresult.like,buttonformget("/viewgenresult/" + genresult.key.urlsafe(),"+"), buttonformpost("/deletegenresult/" + genresult.key.urlsafe(),"Del")] for genresult in getallgenresults(self,user.email())]
            content = htmltable(htmlrows(rows))
            self.response.write(LIST_GENRESULT_TEMPLATE % content)
        else:
            self.response.write('You must login')

        self.response.write('</body></html>')
# [END ListGenresult]


# [START ListGenresult]
class ListGenresultsPageAttr(webapp2.RequestHandler):
    def get(self,attrpage):
        content = []
        (attr,page) = attrpage.split("/")

        user = users.get_current_user()
        if user:
            content.append(html("h1","Results " + attr))
            content.append("Now is " + date2string(localnow()))
            content.append("<hr>")

            query = getgenresultsattr(self,user.email(),attr)
            countresult = query.count()

            # results = [result for result in getgenresultsattr(self,user.email(),attr)]
            ipage   = int(page)
            results = [result for result in query.fetch(9,offset=ipage*9)]

            content.append("Nresults: " + str(countresult))
            content.append("<hr>")
            content.append("Results indices: " + str(ipage*9) + " -> " + str((ipage+1)*9))
            content.append(htmltable(htmlrows( [ [htmllink("/viewgenresult/" + genresult.key.urlsafe(),htmlimage(thumbnailurl(genresult))) for genresult in genresult5] for genresult5 in lsplit(results,3) ] ) ) )
            content.append("<hr>")
            if ipage == 0:
                content.append(htmltable(htmlrow( [buttonformget("/listgenresultspageattr/" + attr + "/1","Next"), buttonformget("/","Home")])))
            else:
                content.append(htmltable(htmlrow( [buttonformget("/listgenresultspageattr/" + attr + "/" + str(int(page)-1),"Prev"), buttonformget("/listgenresultspageattr/" + attr + "/" + str(int(page)+1),"Next"),buttonformget("/","Home")])))
        else:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))

        content = htmlcenter(content)
        writehtmlresponse(self,content)

# [END ListGenresult]



# [START MyListGenresult]
class MyListGenresults(webapp2.RequestHandler):
    def get(self,email):
        content = [",".join([genresult.name,genresult.generationname,genresult.imageurl,genresult.like]) for genresult in getallgenresults(self,email)]
        self.response.write(";".join(content))

# [END MyListGenresult]


# [START AddGenresult]
class AddGenresult(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user == None:
            content = ADD_GENRESULT_TEMPLATE
        else:
            content = 'Sorry, you must login to access this page'

        self.response.write(htmlbody(content))
# [END AddGenresult]

# [START DoAddGenresult]
class DoAddGenresult(webapp2.RequestHandler):
    def post(self):
        genresultname              = self.request.get('genresultname')
        genresultgenerationname    = self.request.get('genresultgenerationname')
        genresultscript            = self.request.get('genresultscript')
        genresultimageurl          = self.request.get('genresultimageurl')
        genresult = addgenresult(self,genresultname,genresultgenerationname,genresultimageurl,users.get_current_user().email())
        self.redirect("/listgenresults")
# [END DoAddChiChar]

# [START DoAddGenresult]
class MyDoAddGenresult(webapp2.RequestHandler):
    def post(self,email):
        genresultname              = self.request.get('genresultname')
        genresultgenerationname    = self.request.get('genresultgenerationname')
        genresultimageurl          = self.request.get('genresultimageurl')
        genresultscript            = self.request.get('genresultscript')
        genresult = addgenresult(self,genresultname,genresultgenerationname,genresultimageurl,genresultscript,email)
        self.redirect("/listgenresults")
# [END DoAddChiChar]


def deletegenresult(request,genresultid):
    genresult_key = ndb.Key(urlsafe=genresultid)
    genresult     = genresult_key.get()
    genresult.key.delete()
    

# [START DeleteGenresult]
class DeleteGenresult(webapp2.RequestHandler):
    def post(self,genresultid):
        deletegenresult(self,genresultid)
        self.redirect("/listgenresults")

# [END DeleteGenresult]


# [START ViewGenresult]
class ViewGenresult(webapp2.RequestHandler):
    def get(self,genresultid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            content.append(html("h1","Description"))
            content.append(htmltable( htmlrows( [ ["Name", genresult.name],["Generation", genresult.generationname],["Image", genresult.imageurl],["Like", genresult.like], ["Render Status", genresult.renderstatus], ["-- Script", genresult.script], ["-- Niter", genresult.renderniter], ["Publish Status", genresult.publishstatus],["-- Title", genresult.publishtitle],["-- Description", genresult.publishdescription], ["-- Categories", genresult.publishcategories], ["-- Tags", genresult.publishtags] ])))
            # content.append(buttonformget())

            likevalue    = iff(genresult.like          == "Yes", "No", "Yes")
            rendervalue  = iff(genresult.renderstatus  == "TODO", "",  "TODO")
            publishvalue = iff(genresult.publishstatus == "TODO", "",  "TODO")

            content.append(htmltable(htmlrow( [buttonformpost("/likegenresult/" + genresult.key.urlsafe()  + "/" + likevalue,"Like"), 
                                               buttonformget("/rendergenresult/" + genresult.key.urlsafe() + "/" + rendervalue,"Render"),
                                               buttonformget("/publishgenresult/" + genresult.key.urlsafe()+ "/" + publishvalue ,"Publish"),buttonformget("/listgenresults","List"), buttonformget("/","Home")])))
            content.append("<hr>")
            content.append(htmlimage(genresult.imageurl))
            content.append("<hr>")

        writehtmlresponse(self,content)

# [START ViewGenresult]
class LikeGenresult(webapp2.RequestHandler):
    def post(self,genresultid,newvalue):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            genresult.like = newvalue
            genresult.put()
        self.redirect("/viewgenresult/" + genresultid)

# [START DoAddGeneration]
class RenderGenresult(webapp2.RequestHandler):
    def get(self,genresultid,newvalue):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            if newvalue == "TODO":
                content.append(htmlform("/dorendergenresult/" + genresult.key.urlsafe(), 
                                        [genresult.name, htmltextarea("renderniter","150000")], 
                                        "Submit"))
                
                writehtmlresponse(self,content)

            else:
                genresult.renderstatus = "MAYBE"
                genresult.put()
                self.redirect("/viewgenresult/" + genresultid)



# [START ViewGenresult]
class DoRenderGenresult(webapp2.RequestHandler):
    def post(self,genresultid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            niter = self.request.get('renderniter')

            genresult.renderstatus = "TODO"
            genresult.renderniter  = niter
            genresult.put()

        self.redirect("/viewgenresult/" + genresultid)
# [END DoAddChiChar]

# [START DoAddGenresult]
class MyDoRenderGenresultEnd(webapp2.RequestHandler):
    def post(self,email):
        genresultname              = self.request.get('genresultname')

        for genresult in Genresult.query(Genresult.name == genresultname):
            genresult.renderstatus = "DONE"
            genresult.put()
            break

        self.redirect("/listgenresults")
# [END DoAddChiChar]





# [START PublishGenresult]
class PublishGenresult(webapp2.RequestHandler):
    def get(self,genresultid,newvalue):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            if newvalue == "TODO":
                content.append(htmlform("/dopublishgenresult/" + genresult.key.urlsafe(), 
                                        [genresult.name, 
                                         htmltextarea("publishtitle",""),
                                         htmltextarea("publishdescription","Generative pattern"),
                                         htmltextarea("publishcategories","Work.Pattern"),
                                         htmltextarea("publishtags","generative.pattern")], 
                                        "Submit"))

                writehtmlresponse(self,content)
            else:
                genresult.publishstatus = "MAYBE"
                genresult.put()
                self.redirect("/viewgenresult/" + genresultid)


# [START DoPublishGenresult]
class DoPublishGenresult(webapp2.RequestHandler):
    def post(self,genresultid):

        content = []
        user = users.get_current_user()
        if user:
            dict_name      = self.request.get('dict_name',USERDICT)
            genresult_key = ndb.Key(urlsafe=genresultid)
            genresult = genresult_key.get()

            publishtitle = self.request.get('publishtitle')
            publishdescription = self.request.get('publishdescription')
            publishcategories = self.request.get('publishcategories')
            publishtags = self.request.get('publishtags')

            genresult.publishstatus = "TODO"
            genresult.publishtitle  = publishtitle
            genresult.publishdescription = publishdescription
            genresult.publishcategories = publishcategories
            genresult.publishtags = publishtags
            genresult.put()

        self.redirect("/viewgenresult/" + genresultid)
# [END DoPublishGenresult]

# [START MyDoPublishGenresultEnd]
class MyDoPublishGenresultEnd(webapp2.RequestHandler):
    def post(self,email):
        genresultname              = self.request.get('genresultname')

        for genresult in Genresult.query(Genresult.name == genresultname):
            genresult.publishstatus = "DONE"
            genresult.put()
            break

        self.redirect("/listgenresults")
# [END MyDoPublishGenresultEnd]


