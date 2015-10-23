from django.conf.urls import patterns, url

from models import FileUpload


# fileupload_list = ListView.as_view(model=FileUpload)

urlpatterns = patterns('',
    url('^file/(?P<path>.+)',  'gridfsuploads.views.serve_from_gridfs', name='upload_file'),
    url('^list/', 'gridfsuploads.views.serve_files_list', name='file_uploading'),
    url('^download/(?P<path>.+)','gridfsuploads.views.download_file',name='download_file'),
    url('^delete/(?P<path>.+)','gridfsuploads.views.delete_file',name='delete_file'),
    url('^cleartemp/(?P<path>.+)','gridfsuploads.views.clear_temp_dir'),
    url('^properties/(?P<path>.+)','gridfsuploads.views.file_properties',name='properties'),
    url('^list/logout/$','gridfsuploads.views.logout', name='logout')
)