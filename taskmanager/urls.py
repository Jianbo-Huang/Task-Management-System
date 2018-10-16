"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import requests
from  tasks  import views
from  tasks  import models
admin.autodiscover()

def stream_response_generator(filters="alltasks") :
     str=""
     if filters=="alltasks" :
        str=models.showtasks()
     elif filters=="allopentasks":
         str=models.showtasks(False)
     elif filters=="showclosed":
         str=models.showclosed()
     return str
urlpatterns = [
    url(r'^home', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^alltasks/', lambda r: HttpResponse(stream_response_generator("alltasks"))),
    url(r'^showclosed/', lambda r: HttpResponse(stream_response_generator("showclosed"))),
    url(r'^allopentasks/', lambda r: HttpResponse(stream_response_generator("allopentasks"))),
    url(r'^reopen',lambda r: HttpResponse(stream_response_generator("mytasks"))),
    url(r'^handle_reopen',views.handle_reopen,name='handle_reopen'), 
    url(r'^hide', lambda r: HttpResponse(stream_response_generator("allopentasks"))),
   url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^user', TemplateView.as_view(template_name= 'user.html'), name='user'),
    url(r'^$', lambda r: HttpResponseRedirect('admin/')),   # Remove this redirect if you add custom views
    path('admin/', admin.site.urls),
    url(r'^advanced_filters/', include('advanced_filters.urls')),
    url(r'^addtask/',views.addtask,name='addtask'), 
    url(r'^gettask',views.gettask,name='gettask'),
    url(r'^mytasks', views.mytasks,name='mytasks'),
    url(r'^close/', views.closemytask,name='closemytask'),
    url(r'^resolution',views.resolution,name='resolution'),
    url(r'^edit/', views.editmytask,name='editmytask'),
    url(r'^assign/', views.assigntask,name='assigntask'),
    url(r'^getassigned/', views.getassigned,name='getassigned'),
    url(r'^delete/', views.deletemytask,name='deletemytask'),
    url(r'^getedit/', views.getedit,name='getedit'),
    url(r'^getdelete/', views.getdelete,name='getdelete'),
    url(r'^changetask/', views.changetask,name='change'),
    url(r'^myopentasks/', views.myopentasks,name='mytasks'),
     url(r'^myclosed', views.myclosedtasks,name='myclosedtasks'),
    path('hello', views.hello, name = 'hello'),
]

admin.site.site_header = settings.SITE_HEADER
