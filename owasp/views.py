from django.contrib.auth.models import User
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotAllowed,HttpResponse
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.http import require_POST
from django.db import connection
from hashlib import sha1
import re
from .regexes import *


code_msg ={"created":1,"username exists already":2,"wrong or bad inputs":3,"SQL_INJECTION":4}

def record_django_user(request):
    username=request.POST["username"]
    password=request.POST["password"]
    confirm_password=request.POST["confirm_password"]
    email=request.POST.get("email",None)

    pattern=Generate_Whole_Pattern(LOGIN_REGEX_PATTERNS)

    compiled = re.compile(pattern,re.UNICODE|re.I)

    matchObj_username=re.search(compiled,username)
    matchObj_pass_confirm=re.search(compiled,confirm_password)
    matchObj_pass=re.search(compiled,password)
    matchObj_email=re.search(compiled,email)

    if matchObj_username or matchObj_pass or matchObj_email or matchObj_pass_confirm :
        return (True,code_msg["SQL_INJECTION"])


    if username and (password==confirm_password) and password:
        user , created = User.objects.get_or_create(username=username,
                                                    defaults={'email':email})
        if created:
            User.set_password(user,password)
            user.save()
            return (user,code_msg["created"])
        else:
            return (user,code_msg["username exists already"])
    else:
        return (False,code_msg["wrong or bad inputs"])





@require_POST
def create_user_view(request):
    context={'AlreadyExists':False,'error':False,'msg':''}
    if request.method == "POST":
            user , code =record_django_user(request)
            if user:
                if code==code_msg["created"]:
                    return HttpResponseRedirect(
                    reverse('base_app:list')
                )
                elif code==code_msg["SQL_INJECTION"]:
                    context['msg']="SQL Injection Detected : Your Request Has Been Ignored."
                    context.update(csrf(request))
                    return render_to_response('base/log.html',context,
                           context_instance=RequestContext(request))

                else:
                    context['AlreadyExists']=True
                    context.update(csrf(request))
                    return render_to_response('base/log.html',context,
                                              context_instance=RequestContext(request))
            else:
                context['error']=True
                context.update(csrf(request))
                return render_to_response('base/log.html',context,
                                            context_instance=RequestContext(request))



@csrf_exempt
def logout(request):
    referer=request.META.get('HTTP_REFERER', '/')
    regex="localhost:8000"
    compiled = re.compile(regex,re.I)
    matchObj = re.search(compiled,referer)
    if not matchObj:
        return render(request,'base/csrf_detection.html',{})
    auth.logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def login(request):
    c={'error':'','user':'','detail':''}
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        pattern=Generate_Whole_Pattern(LOGIN_REGEX_PATTERNS)

        compile = re.compile(pattern,re.UNICODE|re.I)
        matchObj_username = re.search(compile,username)
        matchObj_password = re.search(compile,password)

        if matchObj_password or matchObj_username:
            c['error']="SQL Injection Detected : Your Request Has Been Denied."
            if matchObj_username:
                c['detail']=matchObj_username.group()
            elif matchObj_password:
                c['detail']=matchObj_password.group()
            elif matchObj_username and matchObj_password:
                c['detail']=matchObj_username.group()+" , "+matchObj_password.group()

            return render(request,'base/log.html',c)


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            c['user']=user
            return HttpResponseRedirect(reverse('base_app:list'))

        else:
            c['error'] = 'wrong credentials try again'
            c.update(csrf(request))
            return render_to_response('base/log.html',c,context_instance=RequestContext(request))

    return render(request,'base/log.html',c)


# Login function - Vulnerable Version
# @csrf_exempt
# def login(request):
#     c={'error':'','user':''}
#     if request.method == "POST":
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         cur = connection.cursor()
#         q="select username,password from auth_user where username=\'"+username+"\' and password=\'"+password+"\'"
#         cur.execute(q)
#         valid_credintals =cur.fetchone()
#         if (valid_credintals is None) or (len(valid_credintals)==0):
#             try:
#                 user = User.objects.get(username=username)
#                 if user is not None:
#                     valid = user.check_password(password)
#                     if valid:
#                         user.backend = 'django.contrib.auth.backends.ModelBackend'
#                         auth.login(request,user)
#                         c['user']=user
#                         return HttpResponseRedirect(reverse('base_app:list'))
#                     else:
#                         c['error'] = 'wrong credentials try again'
#                         c.update(csrf(request))
#                         return render_to_response('base/log.html',c,context_instance=RequestContext(request))
#
#                 else:
#                     c['error'] = 'wrong credentials try again'
#                     c.update(csrf(request))
#                     return render_to_response('base/log.html',c,context_instance=RequestContext(request))
#             except:
#                 pass
#
#
#         if (valid_credintals is not None) and (len(valid_credintals)>0):
#             user =User.objects.get(username=str(valid_credintals[0]))
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             auth.login(request,user)
#             c['user']=user
#             return HttpResponseRedirect(reverse('base_app:list'))
#
#         else:
#             c['error'] = 'wrong credentials try again'
#             c.update(csrf(request))
#             return render_to_response('base/log.html',c,context_instance=RequestContext(request))
#
#     return render(request,'base/log.html',c)

def test(request):
    context={}
    t=get_template('base/404.html')
    html = t.render(Context({'name':'soheil'}))
    return HttpResponse(html)

def home(request):
    return render(request,"base/index.html",None)