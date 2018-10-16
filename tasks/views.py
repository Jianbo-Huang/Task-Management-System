from django.shortcuts import render
from django.http import HttpResponse
from  tasks.models  import *

from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import *



active_user="none"
# Create your views here.

def hello(request):
   text = "<h1>welcome to my app  number </h1>"
   return HttpResponse(text)

def addtask(request):
   models.current_user=request.user.username
   active_user=request.user.username
   print ("current user:",models.current_user)
   return render(request, "addtask.html", {})

def assigntask(request):
   user=request.user
   issuper=user.is_superuser
   print("user,issuper",user,issuper)

   if not issuper:
      text = "<h2>You must be a super user to assign a task</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
   return render(request, "assigntask.html", {})

def getassigned(request):
   id =str( request.POST.get('taskid'))
   i=gettask_byid(id)
   if  i<0:
      text="<h2>Specified task id: "+id+" not exists.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
   state=usertasks[i].status
   if state=="closed":
      text="<h2>Specified task is closed.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
   newowner=str( request.POST.get('newowner'))
   if newowner==usertasks[i].owner:
      text="<h2>Specified owner already owns the task</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
   usertasks[i].owner=newowner
   write_taskdbs()
   text="<h2>Specified task "+id+" is assigned to: "+newowner+"</h2><p>"
   text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
   return HttpResponse(text)

def closemytask(request):
    return render(request, "closetask.html", {})
def editmytask(request):
    return render(request, "edittask.html", {})

def deletemytask(request):
    return render(request, "deletetask.html", {})

def gethtml_body():
    str="<body>\n<div>\n<form>\n<p>\n\
      <a href=\"http://localhost:8000/user\" ><b> Go To Task Manager</a></b>\n</p>\n"
    return str

def mytasks(request,showclosed=True):
    ss=gethtml_body()
    #current_user=str(request.user)
    current_user=request.user.username
    print("current user:",current_user)
    for tsk in usertasks:
      if tsk.status=="deleted":
        continue
      if tsk.owner==current_user:
        if tsk.status=="to-do" or tsk.status=="in progress" or showclosed:
          ss=ss+showtask(tsk)
    ss=ss+"</body>\n</html>"
    return  HttpResponse(ss)
def myopentasks(request):
    return mytasks(request,False)
def myclosedtasks(request):
    ss=gethtml_body()
    #current_user=str(request.user)
    current_user=request.user.username
    for tsk in usertasks:
      if tsk.status=="deleted":
        continue
      if tsk.owner==current_user:
        if tsk.status=="closed":
          ss=ss+showtask(tsk)
    ss=ss+"</body>\n</html>"
    return  HttpResponse(ss)

def gettask(request):
    task=usertask()
    user=request.user.username
    task.owner=user
    #print("user",user)
    #print ("owner",task.owner)
    title = request.POST.get('title')
    task.title=title  
    priority=request.POST.get('priority')
    task.priority=priority
    describe= request.POST.get('describe')
 
    task.desc=describe   
    usertasks.append(task)
    write_taskdbs()
    print("no tasks:",len(usertasks))
    text = "<h2>Your task has been submitted!</h2><p>"
    text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
    return HttpResponse(text)



def pass_parm(request,taskid):
    context= {
        'taskid': taskid,
        }
    return render(request, 'changetask.html', context)

current_task=-1
def getedit(request):
    global current_task
    id =str(request.POST.get('taskid'))
    i=gettask_byid(id)
    if  i<0:
       text="<h2>Specified task id not exists.</h2><p>"
       text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
       return HttpResponse(text)
    user=request.user.username
    current_task=i
    if usertasks[i].owner !=user:
      text = "<h2>Specified task  "+id+" is not owned by you.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
    if usertasks[i].status =="closed" or usertasks[i].status =="deleted":
      text = "<h2>Cannot edit closed or deleted tasks.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
    text="<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
    text=text+"<b>Task ID:</b>"+id+"<p>" 
    text=text+"<form action=\"http://localhost:8000/changetask/\" method=\"POST\">"
    #text=text+" {% csrf_token %}"
    text=text+"<p> <b>Title:</b><input type=\"text\" name=\"title\" size=\"60\""   
   
    text=text+"value=\""+usertasks[i].title+"\" ></p>"
    text=text+"<b><p>Priority (options:normal,low,high,urgent)</b><input type=\"text\" \
name=\"priority\" size=\"20\" value="+usertasks[i].priority+"></p>"

    text=text+"<p><b>Description:</b></p>"
    text=text+"<textarea name=\"describe\" cols=\"70\" rows=\"10\">"+usertasks[i].desc+"</textarea>"
   
    text=text+"<p><input type=\"submit\" value=\"Submit\" /></p>"    
    return HttpResponse(text)

def getdelete(request):
    global current_task
    id =str(request.POST.get('taskid'))
    i=gettask_byid(id)
    if  i<0:
       text="<h2>Specified task id not exists.</h2><p>"
       text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
       return HttpResponse(text)
    user=request.user.username
    current_task=i
    if usertasks[i].owner !=user:
      text = "<h2>Specified task is not owned by you.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
    if usertasks[i].status =="closed" or usertasks[i].status =="deleted":
      text = "<h2>Cannot change closed or deleted tasks.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
    usertasks[i].status="deleted"
    print ("task state:",usertasks[i].status)
    write_taskdbs()
    text = "<h2>Specified task deleted!.</h2><p>"
    text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
    return HttpResponse(text)


@csrf_exempt

def changetask(request):
  i=current_task
  print ("active task:",i)
  usertasks[i].status="in progress"
  usertasks[i].dmodify=str(datetime.date.today())
  title=request.POST.get("title")
  usertasks[i].title=title
  desc=request.POST.get("describe")
  usertasks[i].desc=desc
  priority=request.POST.get("priority")
  usertasks[i].priority=priority
  write_taskdbs()
  
  text = "<h2>Specified task change has been saved!</h2><p>"
  text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
  return HttpResponse(text)


def resolution(request):
    id =str( request.POST.get('taskid'))
    i=gettask_byid(id)
    if  i<0:
       text="<h2>Specified task id not exists.</h2><p>"
       text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
       return HttpResponse(text)
    user=request.user.username
    if usertasks[i].owner !=user:
      text = "<h2>Specified task is not owned by you.</h2><p>"
      text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
      return HttpResponse(text)
    usertasks[i].status="closed"
    usertasks[i].dmodify=str(datetime.date.today())
    usertasks[i].resolve=request.POST.get("resolution")
    write_taskdbs()
  
    text = "<h2>Specified task "+id+"  has been closed!</h2><p>"
    text=text+"<a href=\"http://localhost:8000/user/\"><b> Goto task manager page</a></b></p>"
    return HttpResponse(text)


def handle_reopen(request):
     uname=request.user.username
     if uname !=current_user:
         return None
     klist=request.form
     for k,v in klist:
         for tsk in models.usertasks:
            if k==tsk.id:
               tsk.status="in progress"
     models.writedbs()


