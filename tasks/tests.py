#!/usr/bin/env python
# coding=utf8
from django.test import TestCase
import pickle
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import  pickle
import datetime
import os
import io
import sqlite3
from sqlite3 import Error
 
def exists(path):
   if os.path.isfile (path) :
      return True
   return False

current_user="none"
usertasks=[]
taskids=[0]

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
        self.desc=desc
    def adddesc(self,desc):
       self.desc=descr
   



def loaddbs():
      if exists("taskdbs.dbs"):
         print ("task dbs exists")
         with open('taskdbs.dbs','rb') as f:
           vv=pickle.load(f)
           print("number of items:",len(vv))
           print(vv[0][0],vv[1][0])
           return vv
      
         
def writedbs():
    with open('taskdbs.dbs', 'wb') as f:
      utit=[]
      udate=[]
      for v in usertasks:
        utit.append(v.title)
        udate.append(v.dopen)
      vv=[utit,udate]
      pickle.dump(vv, f)


def write_taskdbs():
  uid=[]
  utit=[]
  uopen=[]
  uowner=[]
  umod=[]
  ustat=[]
  uown=[]
  udesc=[]
  for v in usertasks:
    uid.append(v.id)
    utit.append(v.title)
    uopen.append(v.dopen)
    uown.append(v.owner)
    umod.append(v.dmodify)
    ustat.append(v.status)
    udesc.append(v.desc)
  vv=[uid,utit,uopen,umod,uown,ustat,udesc]
  with open('taskdbs.dbs', 'wb') as f:
    pickle.dump(vv, f)
       
   
def load_taskdbs():
  if exists("taskdbs.dbs"):
    print ("model file exists")
    with open('taskdbs.dbs','rb') as f:
       vv= pickle.load(f)
       uid=vv[0]
       utit=vv[1]
       uopen=vv[2]
       uown=vv[3]
       umod=vv[4]
       ustat=vv[5]
       udesc=vv[6]
       task=usertask()
       for i in range(len(utit)):        
         task.id=uid[i]
         task.title=utit[i]
         print("i,id,tit",i,uid[i],utit[i]
         task.dopen=uopen[i]
         task.owner=uown[i]
         task.dmodify=umod[i]
         task.status=ustat[i]
         task.desc=udesc[i]
         usertasks.append(task)

def gettask():
      klist=request.form
      print (klist)
      print ("cuser:",current_user)
      task=usertask()
      for k,v in klist.items():
          if k=="title":
            task.title=v
          if k=="priority":
             task.priority=v
          if k=="desc":
            task.desc=v
      usertasks.append(task)
      write_taskdbs()



def makeheader(title="Task list for all users"):
     str="<!DOCTYPE html>\n<html>\n\
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n\
<head>\n\
<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />\n\
<title>"+title+"</title>\n\
<meta name=\"keywords\" content=\"cloud computing,optimization,simulation,SaaS,PaaS,marketing,service\" />\n\
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n\</head>"
     return str

def showtask(utask):
   str="<b>Task ID:</b>"+utask.id+"  <b>Title:</b> "+utask.title+"\n"
   str=str+"<p><b>Owner:</b> "+utask.owner+"<b> Created at:</b>" +utask.dopen+" <b> Last Modification:</b> "
   str=str+utask.dmodify+"<b>  Status: </b>"+utask.status+" </p>\n"
   str=str+"<b>Description: </b>"
   str=str+utask.desc+"\n"
   return str

def gethtml_body():
    str="<body>\n<div>\n<form>\n<p>\n\
      <a href=\"http://localhost:8000/user\" ><b> Go To Task Manager</a></b>\n</p>\n"
    return str

def showtasks(showclosed=True):
     #ss=makeheader("Tasks list")
     ss=gethtml_body()
     for tsk in usertasks:
         if tsk.status=="to-do" or tsk.status=="in progress" or showclosed:
            ss=ss+showtask(tsk)
     ss=ss+"</body>\n</html>"
     return ss

def showmytasks(showclosed=True):
    #ss=makeheader("My Tasks list")
    ss=gethtml_body()
    for tsk in usertasks:
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
   #ss=makeheader("Re-open Task")
   ss=gethtml_body()
   mtsks=get_my_tasks("closed")
   ss+=html_options("hand_reopen","Re-open-task",mtsks)
   ss=ss+"</body>\n</html>"
   return ss

# Create your tests here.
x=["abc","def","ghi"]
x1=x
x2=["hhh","jjj","kkk"]
y=[x,x1,x2,x2]
with open("ttt.p","wb") as f:
     pickle.dump(y,f)
     
load_taskdbs()
task1=usertask()
usertasks.append(task1)
task2=usertask()
usertasks.append(task2)
task3=usertask()
usertasks.append(task3)
write_taskdbs()


#str=showtasks()
#print (str)
 

print("Number of defined tasks:",len(usertasks))




     
