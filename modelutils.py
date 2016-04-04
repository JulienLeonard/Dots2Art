from utils     import *
from myschemas import *
from mydicts   import *
from timeutils import *

from utils     import *
from myschemas import *
from mydicts   import *
from timeutils import *

def getgeneration(generationname,email):
    generations_query = Generation.query(Generation.name == generationname).filter(Generation.email == email)
    qresult = generations_query.fetch(1)
    if len(qresult) > 0:
        return qresult[0]
    return None

def getallgenerations(request,email):
    dict_name = request.request.get('dict_name', USERDICT)
    return Generation.query(ancestor=dict_key(dict_name)).filter(Generation.email == email).order(-Generation.date)

def getgenerationstodo(request,email):
    dict_name = request.request.get('dict_name', USERDICT)
    return Generation.query(ancestor=dict_key(dict_name)).filter(Generation.email == email).filter(Generation.status == "TODO").order(-Generation.date)


def getgenresults(generationname,email):
    return Genresult.query(Genresult.generationname == generationname).filter(Genresult.email == email).order(-Generation.date)


def getallgenresults(request,email):
    dict_name = request.request.get('dict_name', USERDICT)
    return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).order(-Genresult.date)


def getgenresultsattr(request,email,attr):
    dict_name = request.request.get('dict_name', USERDICT)
    if attr == "new":
        return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.like == "No").order(-Genresult.date)
    if attr == "like":
        return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.like == "Yes").order(-Genresult.date)
    if attr == "torender":
        return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.renderstatus == "TODO").order(-Genresult.date)
    if attr == "topublish":
        return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.publishstatus == "TODO").order(-Genresult.date)



def thumbnailurl(genresult):
    return "http://dl.dropboxusercontent.com/u/78965321/site/genresult/" + genresult.name + "thumb.png"

def getgenresultstorender(request,email):
    dict_name = request.request.get('dict_name', USERDICT)
    return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.renderstatus == "TODO").order(-Genresult.date)

def getgenresultstopublish(request,email):
    dict_name = request.request.get('dict_name', USERDICT)
    return Genresult.query(ancestor=dict_key(dict_name)).filter(Genresult.email == email).filter(Genresult.publishstatus == "TODO").order(-Genresult.date)


# def getallroutinechecks(request,email):
#     dict_name = request.request.get('dict_name', USERDICT)
#     return RoutineCheck.query(ancestor=dict_key(dict_name)).filter(RoutineCheck.email == email).order(-RoutineCheck.date)

# def getallroutinechecksafterdate(request,email,mindate):
#     dict_name    = request.request.get('dict_name', USERDICT)
#     return RoutineCheck.query(ancestor=dict_key(dict_name)).filter(RoutineCheck.email == email).filter(RoutineCheck.date >= mindate)

# def getallroutinecheckstoday(request,email):
#     return getallroutinechecksafterdate(request,email,utcnowdayrange()[0])

# def getallroutinechecksndays(request,email,ndays):
#     dateranges = getlastdaymidnightrangesutc(localnow(),ndays)
#     return getallroutinechecksafterdate(request,email,dateranges[0][0])

# def getallallroutinechecks(request):
#     dict_name = request.request.get('dict_name', USERDICT)
#     return RoutineCheck.query(ancestor=dict_key(dict_name)).order(-RoutineCheck.date)

# def getroutines(goalname,email):
#     return Routine.query(Routine.goalname == goalname).filter(Routine.email == email)

# def getroutinechecks(routinename,allroutinecheckdata):
#     # return RoutineCheck.query(RoutineCheck.routinename == routinename).fetch()
#     # return [routinecheck for routinecheck in allroutinechecks if routinecheck.routinename == routinename]
#     return [routinecheck for routinecheck in allroutinecheckdata if routinecheck[0] == routinename]

# def getdateroutinechecks(routinename,allroutinecheckdata,utcdaterange):
#     result = []
#     for routinecheck in getroutinechecks(routinename,allroutinecheckdata):
#         if isdateinrange(utcdaterange,routinecheck[1]):
#             result.append(routinecheck)
#     return result

# #
# # can be NA, OK or KO
# #
# def getroutinestatus(routine,allroutinecheckdata,utcdaterange):
#     routinechecks = getdateroutinechecks(routine.name,allroutinecheckdata,utcdaterange)
#     if len(routinechecks) > 0:
#             return "OK"
#     else:
#         if routine.status == "NA" or routine.date > utcdaterange[0]:
#             return "NA"
#         else:
#             # check frequency covering
#             newutcdaterange = (utcdaterange[0] - datetime.timedelta(getroutinedayfrequency(routine)-1),utcdaterange[1])
#             freqroutinechecks = getdateroutinechecks(routine.name,allroutinecheckdata,newutcdaterange)
            
#             if len(freqroutinechecks) > 0:
#                 return "COVER"
#             else:
#                 return "KO"


# def getroutinedayfrequency(routine):
#     if "every day" in routine.description:
#         return 1
#     if "every week" in routine.description:
#         return 7
#     if "every month" in routine.description:
#         return 31
#     if "every 2 days" in routine.description:
#         return 2
#     return 1

# def addroutinecheck(request,routinename,value="True"):
#     user = users.get_current_user()
#     if user:
#         dict_name = request.request.get('dict_name', USERDICT)
#         oroutinecheck = RoutineCheck(parent=dict_key(dict_name))
#         oroutinecheck.routinename        = routinename
#         oroutinecheck.email              = user.email()
#         oroutinecheck.value              = value
#         oroutinecheck.put()
#     return oroutinecheck

# def addroutinecheckdate(request,routinename,date,value):
#     user = users.get_current_user()
#     if user:
#         dict_name = request.request.get('dict_name', USERDICT)
#         oroutinecheck = RoutineCheck(parent=dict_key(dict_name))
#         oroutinecheck.routinename        = routinename
#         oroutinecheck.email              = user.email()
#         oroutinecheck.date               = date
#         oroutinecheck.value              = value
#         oroutinecheck.put()
#     return oroutinecheck
