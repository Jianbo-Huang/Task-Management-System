from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import  pickle
import datetime
import os

def exists(path):
   if os.path.isfile (path) :
      return True
   return False

current_user="none"
usertasks=[]

def gettask_byid(id):
   for i in range(len(usertasks)):
      if  usertasks[i].id==id:
         return i
   return -1
   
def get_my_tasks(sel="open"):
    mytasks={}   
    for tsk in usertasks:
      select=False
      if sel=="closed" and tsk.status=="closed":
        select=True
      elif sel=="open" or sel=="to-do" or sel=="in progress":
        if tsk.status=="to-do" or tsk.status=="in progress":
          select=True
      if tsk.owner==current_user and select:
        id=tsk.id
        mytasks[id]=tsk.title
    return mytask
   
def newid():
    id=len(usertasks)+1
    return str(id)
    
class  usertask:
    def __init__(self, title="none",desc="none"):
        self.id=newid()
        self.title= title
        self.dopen=str(datetime.date.today())
        self.dmodify=self.dopen  #last modification time
        self.status="to-do"
        self.owner=current_user
        self.priority="normal"
        self.desc=desc
        self.resolve="none"
    def adddesc(self,desc):
       self.desc=descr
 
def write_taskdbs():
  uid=[]
  utit=[]
  uopen=[]
  uown=[]
  umod=[]
  ustat=[]
  uown=[]
  prio=[]
  udesc=[]
  resolve=[]
  for v in usertasks:
    uid.append(v.id)
    utit.append(v.title)
    uopen.append(v.dopen)
    uown.append(v.owner)
    umod.append(v.dmodify)
    ustat.append(v.status)
    prio.append(v.priority)
    udesc.append(v.desc)
    resolve.append(v.resolve)
  vv=[uid,utit,uopen,uown,umod,ustat,prio,udesc,resolve]
  with open('taskdbs.dbs', 'wb') as f:
    pickle.dump(vv, f)
       
   
def load_taskdbs():
  if exists("taskdbs.dbs"):
    print ("model file exists")
    print("number of tasks before:",len(usertasks))
    with open('taskdbs.dbs','rb') as f:
       vv= pickle.load(f)
       uid=vv[0]
       utit=vv[1]
       uopen=vv[2]
       uown=vv[3]
       umod=vv[4]
       ustat=vv[5]
       prio=vv[6]
       udesc=vv[7]
       resolve=[]
       if len(vv)>8:
          resolve=vv[8]
       for i in range(len(utit)):
         task=usertask()      
         task.id=uid[i]
         task.title=utit[i]
         task.dopen=uopen[i]
         task.owner=uown[i]
         task.dmodify=umod[i]
         task.status=ustat[i]
         task.priority=prio[i]
         task.desc=udesc[i]
         if len(resolve)==len(utit):
           task.resolve=resolve[i]
         usertasks.append(task)
         #print("owner:",task.owner)
    print("number of tasks now:",len(usertasks))
   
         

def makeheader(title="Task list for all users"):
     str="<!DOCTYPE html>\n\
    <html>\n\
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n\
<head>\n\
<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />\n\
<title>"+title+"</title>\n\
<meta name=\"keywords\" content=\"cloud computing,optimization,simulation,SaaS,PaaS,marketing,service\" />\n\
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n\</head>\
"
     return str
     
def showtask(utask,showres=False):
   str="<b><font color=\"blue\">Task ID:"+utask.id+" </b> <b><font color=\"black\">Title:</b> "+utask.title+"\n"
   str=str+"<p><b>Owner:</b> "+utask.owner+"<b>   Priority:</b>"+utask.priority +"<b>   Created at:</b>" +utask.dopen+" <b> Last Modification:</b> "
   str=str+utask.dmodify+"<b>  Status: </b>"+utask.status+" </p>\n"
   str=str+"<p><b>Description: </b>"
   str=str+utask.desc+"</p>\n"
   if  showres:
      str=str+"<p><b>Resolution: </b>"
      str=str+utask.resolve+"</p>\n"
   return str

def gethtml_body():
    str="<body>\n<div>\n<form>\n<p>\n\
      <a href=\"http://localhost:8000/user\" ><b> Go To Task Manager</a></b>\n</p>\n"
    return str

def showtasks(showclosed=True):
     ss=gethtml_body()
     #print("no tasks in showing:",len(usertasks))
     for i in range(len(usertasks)):
         tsk=usertasks[i]
         if tsk.status=="deleted":
            continue
         if tsk.status=="to-do" or tsk.status=="in progress" or showclosed:
            ss=ss+showtask(tsk,True)
     ss=ss+"</body>\n</html>"
     return ss

def showclosed():
     ss=gethtml_body()
     for i in range(len(usertasks)):
       tsk=usertasks[i]
       if tsk.status!="closed":
         continue
       ss=ss+showtask(tsk,True)
     ss=ss+"</body>\n</html>"
     return ss

def showmytasks(showclosed=True):
    ss=gethtml_body()
    print("current user:",current_user,active_user)
    for tsk in usertasks:
      if tsk.status=="deleted":
         continue
      if tsk.owner==current_user:
        if tsk.status=="to-do" or tsk.status=="in progress" or showclosed:
          ss=ss+showtask(tsk)
    ss=ss+"</body>\n</html>"
    return ss
     
def http_options(action,optname,values):
   str="<form action=\""+action+"\" method=\"POST\">\n<p>\n"
   str=str+optname+"<input type=\"text\" name=\""+optname+"\">\n" 
   str=str+"<select name=\"select\" type=\"text\">\n"
   for k,v in values:
     s1="<option value=\""+k+"\">"+v+"</option>\n"
     str+=s1
   str+="</select>\n</p>"
   str+="<p>\n<input type=\"submit\" value=\"Submit\" style=\"font-size : 20px;border-style:none;background-color:lightblue\"/>"
   str+="</p>\n</form>\n"

def reopentask():
   ss=gethtml_body()
   mtsks=get_my_tasks("closed")
   ss+=html_options("hand_reopen","Re-open-task",mtsks)
   ss=ss+"</body>\n</html>"
   return ss
   
load_taskdbs()
print("Number of defined tasks:",len(usertasks))

class Task(models.Model):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )

    PRIORITIES = (
        ('00_low', _('Low')),
        ('10_normal', _('Normal')),
        ('20_high', _('High')),
        ('30_critical', _('Critical')),
        ('40_blocker', _('Blocker'))
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.id, self.title)


class Item(models.Model):
    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Check List")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item_description = models.CharField(_("description"), max_length=200)
    is_done = models.BooleanField(_("done?"), default=False)

    def __str__(self):
        return self.item_description

