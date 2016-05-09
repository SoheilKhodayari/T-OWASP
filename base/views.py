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
from django.views.decorators.http import require_POST,require_GET
from .models import *
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
import os
import mimetypes
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from urllib import urlencode
from .search import *
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from owasp.regexes import *

@login_required()
@require_GET
def upload_view(request):
    return render(request,'base/upload.html',None)

@require_POST
def upload(request):
    user = request.user
    file = request.FILES['files[]']
    public = request.POST.get('public',False)

    if file != None:
        fs = FileStorage.objects.create(user=user,file=file,public=public)
        return HttpResponseRedirect(reverse('base_app:list'))

    ctx= {'error':'no file attached'}
    return render(request,'base/upload.html',ctx)

def download_view(request):
    return render(request,'base/download.html',None)

class FileDetailView(DetailView):
    model = FileStorage
    pk_url_kwarg = 'filePK'
    template_name = 'base/download.html'


def download(request,filePK):
    storage = get_object_or_404(FileStorage,pk=filePK)
    file_name = os.path.basename(storage.file.name)
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response


def file_list_view(request):
    try:
        if not request.user.is_authenticated()  :
            d = {'server_message':"Not Logged In."}
            query_str = urlencode(d)
            return HttpResponseRedirect('/login/?' +query_str)
    except:
            d = {'server_message':"Not logged in"}
            query_str = urlencode(d)
            return HttpResponseRedirect('/login/?' +query_str)
    if request.method == 'GET':
        if request.GET.get("submit_search_button"): # if search submit button clicked
            query_string = ''
            found_entries = None
            if ('q' in request.GET) and request.GET['q'].strip():
                query_string = request.GET['q']


                whole_regex= Generate_Whole_Pattern(XSS_COMPLETE_REGEX_LIST)
                re_compiled = re.compile(whole_regex,re.UNICODE|re.I)
                matchObj = re.search(re_compiled,query_string)
                if matchObj:
                    response =  render_to_response('base/list.html',
                             { 'error':'probable xss attack detected : X_XSS_Protextion Activated' },
                             context_instance=RequestContext(request))

                    response['X-XSS-Protection']= '1'
                    return response



                entry_query = get_query(query_string, ['file'])

                found_entries = FileStorage.objects.filter(entry_query)
                found_entries=found_entries.filter(user=request.user)
                num = len(found_entries)
            query_string = mark_safe(query_string)
            response= render_to_response('base/list.html',
                          { 'query_string': query_string, 'files': found_entries,'num':num },
                             context_instance=RequestContext(request))
            response['X-XSS-Protection']= '1'
            return response

        # handling the page controller view
        files = FileStorage.objects.filter(user=request.user)
        ctx = {'files': files}
        ctx.update(csrf(request))
        return render_to_response(
            'base/list.html',
            ctx,
            context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect(reverse('error'))


def public_file_list_view(request):
    if request.method == 'GET':
        if request.GET.get("submit_search_button"):
            query_string = ''
            found_entries = None
            if ('q' in request.GET) and request.GET['q'].strip():
                query_string = request.GET['q']


                # XST Cross Site Tracing Prevented by paranoid matching
                # <script>
                # var xmlhttp = new XMLHttpRequest();
                # var url = 'http://127.0.0.1/';
                #
                # xmlhttp.withCredentials = true; // send cookie header
                # xmlhttp.open('TRACE', url, false);
                # xmlhttp.send();
                # </script>


                whole_regex= Generate_Whole_Pattern(XSS_COMPLETE_REGEX_LIST)
                re_compiled = re.compile(whole_regex,re.UNICODE|re.I)
                matchObj = re.search(re_compiled,query_string)
                if matchObj:
                    response =  render_to_response('base/public-list.html',
                             { 'error':'probable xss attack detected: X_XSS_Protextion Activated.' },
                             context_instance=RequestContext(request))

                    response['X-XSS-Protection']= '1'
                    return response



                entry_query = get_query(query_string, ['file','user__username'])

                found_entries = FileStorage.objects.filter(entry_query)
                found_entries=found_entries.filter(public=True)
                num = len(found_entries)
            query_string = mark_safe(query_string)
            response =  render_to_response('base/public-list.html',
                          { 'query_string': query_string, 'files': found_entries,'num':num },
                             context_instance=RequestContext(request))
            response['X-XSS-Protection']= '1'
            return response

        # handling the page controller view
        files = FileStorage.objects.filter(public=True)
        ctx = {'files': files}
        return render(request,
            'base/public-list.html',
            ctx,
            )
    else:
        return HttpResponseRedirect(reverse('error'))

def create_note_object(request):
    body=request.POST['body']
    public=request.POST.get('public',False)
    subject=request.POST['subject']
    title=request.POST['title']

    pattern=Generate_Whole_Pattern(LOGIN_REGEX_PATTERNS)
    compile = re.compile(pattern,re.UNICODE|re.I)
    #matchObj_body=re.search(compile,body)
    matchObj_subject=re.search(compile,subject)
    matchObj_title=re.search(compile,title)
    if matchObj_subject or matchObj_title :
        return None
    path = settings.MEDIA_ROOT
    filename = title + '.txt'
    with open(os.path.join(path, filename), 'wb+') as f:
        f.write(subject)
        f.write("\n")
        f.write(body)
        f.close()
    file = path + '/'+filename
    note = Note.objects.create(user=request.user,body=body,public=public,subject=subject,title=title,file=file)

    return note

@login_required()
def create_note_view(request):
    ctx = {"error":''}
    if request.method =="GET":
        return render(request,"base/create_note.html",None)
    if request.method =="POST":
        try:
            note = create_note_object(request)
            if not note:
                return render(request,"base/create_note.html",{'msg':'Sql Injection Detected: Request Denied'})
            return HttpResponseRedirect(reverse('base_app:note-list'))
        except:
            ctx['error']='fatal error ocurred , try again'
            return render(request,"base/create_note.html",ctx)

    return HttpResponseRedirect(reverse('error'))

class NoteDetailView(DetailView):
    model = Note
    pk_url_kwarg = 'notePK'
    template_name = 'base/noteDetail.html'

@login_required()
def notes_list_view(request):
        notes = Note.objects.filter(user=request.user)
        ctx = {'notes': notes}
        ctx.update(csrf(request))
        return render_to_response(
            'base/noteList.html',
            ctx,
            context_instance=RequestContext(request)
            )

def downloadNote(request,notePK):
    storage = get_object_or_404(Note,pk=notePK)
    file_name = os.path.basename(storage.file.name)
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

def xss_test(request):
    name = request.GET.get('name',False)
    t=get_template('base/xss.html')
    name=name
    html = t.render() + "%s"%name
    response = HttpResponse(html)
    response['X-XSS-Protection']= '0'
    return response

@login_required()
def show_file_view(request):
    return render(request,'base/SearchShowFile.html',{})

@require_GET
def dump_file(request):
    ctx={'error':''}
    if request.GET.get('submit'):
        BASE_PATH = os.path.dirname(os.path.dirname(__file__))
        filename = request.GET.get('filename',False)
        referer=request.META.get('HTTP_REFERER', '/')
        regex="http://localhost:8000/storage/showFileSearch/"
        compiled = re.compile(regex,re.I)
        matchObj = re.search(compiled,referer)
        if not matchObj:
            ctx['error']='LDAP Injection Detected , Please Stop Hammering!'
            return render(request,'base/SearchShowFile.html',ctx)
        if not filename:
            return HttpResponseRedirect(reverse('base_app:show-file'))

        media = os.path.join(BASE_PATH,'media')

        #sanitize file name
        dt_regex = "(\.\.\/) |(\.\.)"
        dt_regex_compiled = re.compile(dt_regex,re.I)
        matchObj = re.search(dt_regex_compiled,filename)
        if matchObj:
            ctx['error']='Directory Traversal Detected , Please Stop Hammering!'
            return render(request,'base/SearchShowFile.html',ctx)

        try:
            filename = os.path.join(media,filename)
            content = open(filename).read()
            context={'content':content}
            return render_to_response('base/ShowNote.html',context,context_instance=RequestContext(request))
        except:
            ctx['error']='no such file exists'
            return render(request,'base/SearchShowFile.html',ctx)

