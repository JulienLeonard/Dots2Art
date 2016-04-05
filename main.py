#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from maintemplates import *
from generation    import *
from genresult     import *
from utils         import *
from htmlutils     import *
from modelutils    import *
from timeutils     import *
# import pytz


class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        content = []
        url = users.create_login_url(self.request.uri)
        if not user:
            url_linktext = 'Login'
            content.append(htmllink(url,url_linktext))
        else:
            content.append(html("h1","Dashboard"))
            content.append("Now is " + date2string(localnow()))
            content.append("<hr>")
            content.append(htmltable(htmlrow([buttonformget("/listgenerations","Generations"),buttonformget("/logs","Logs"),buttonformget("/export","Exports")])))
            content.append("<hr>")
            content.append(html("h2","Results"))
            content.append(htmltable(htmlrow([buttonformget("/listgenresults/new","New"),buttonformget("/listgenresults/like","Likes"),buttonformget("/listgenresultspageattr/torender/0","To render"),buttonformget("/listgenresultspageattr/topublish/0","To publish")])))
            content.append("<hr>")
            url_linktext = 'Logout'
            content.append(htmllink(url,url_linktext))
        
        content = htmlcenter(content)
        writehtmlresponse(self,content)

class MyListLikes(webapp2.RequestHandler):
    def get(self,email):
        query       = getgenresultsattr(self,email,"like")
        results     = [result.name for result in query]
        self.response.write(";".join(results))
        
class MyListJobs(webapp2.RequestHandler):
    def get(self,email):
        jobs = []
        jobs = jobs + [["publish",genresult.name,str(genresult.publishtitle),str(genresult.publishdescription),str(genresult.publishcategories).replace(",","."),str(genresult.publishtags).replace(",",".")] for genresult in getgenresultstopublish(self,email)]
        jobs = jobs + [["render",genresult.name,str(genresult.script),str(genresult.renderniter)]          for genresult  in getgenresultstorender(self,email)]
        jobs = jobs + [["generation",generation.name,generation.script,generation.niter,generation.status] for generation in getgenerationstodo(self,email)]
        jobs = [",".join(job) for job in jobs]
        self.response.write(";".join(jobs))

            


# handlers = [('/', MainHandler)] + generationhandlers() + genresulthandlers()
handlers = [('/', MainHandler),('/mylistjobs/(.*)', MyListJobs),('/mylistlikes/(.*)', MyListLikes)] + generationhandlers() + genresulthandlers()

app = webapp2.WSGIApplication(handlers, debug=True)
