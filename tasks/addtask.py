import pickle
import datetime

current_user="none"
usertasks=[]

class  usertask:
    def __init__(self, title,owner):
        self.title= title
        self.dopen=datetime.datetime.now()
        self.dmodify=self.dopen  #last modification time
        self.status="to-do"
        self.owner=current_user
        self.content="none"
    def adddesc(self,desc):
       self.content=descr
    
tsk=usertask("task 1","jhuang")
tsk2=usertask("task 2","jhuang")
tsk3=usertask("task 3","jhuang")

def load_taskdbs():
  with open('taskdbs.dbs') as f:
         if (f is not None):
            usertasks= pickle.load(f)
         else:
            print("no input file")
         
def write_taskdbs():
      with open('taskdbs.dbs', 'wb') as f:
          pickle.dump(usertasks, f)

usertasks=[tsk,tsk2,tsk3]
print (tsk.title,tsk.owner,tsk.dopen)
print(usertasks[0].title)
write_taskdbs()

k=open("pwds")
