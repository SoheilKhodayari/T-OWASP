
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *


urlpatterns = [
    url(r'^upload/$',upload_view,name='upload-view'),
    url(r'^list/$',file_list_view,name='list'),
    url(r'^publicList/$',public_file_list_view,name='public-list'),
    url(r'^Post_Upload/$',upload,name='post-upload'),
    url(r'^download(?P<filePK>[\w]+)/$',FileDetailView.as_view(),name='download-view'),
    url(r'^Get_Download(?P<filePK>[\w]+)/$',download,name='get-download'),

    url(r'^noteList/$',notes_list_view,name='note-list'),
    url(r'^createNote/$',create_note_view,name='create-note'),
    url(r'^detailNote(?P<notePK>[\w]+)/$',NoteDetailView.as_view(),name='note-detail'),
    url(r'^Get_NoteDownload(?P<notePK>[\w]+)/$',downloadNote,name='get-note-download'),

    url(r'^xss/$',xss_test,name='xss-test'),
    url(r'^showFile/$',dump_file,name='show-file'),
    url(r'^showFileSearch/$',show_file_view,name='show-file-search'),
    ]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


