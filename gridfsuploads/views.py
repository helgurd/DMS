from mimetypes import guess_type

from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect

from gridfs.errors import NoFile
from gridfsuploads import gridfs_storage
from gridfsuploads.models import FileUpload, UserFiles

from pymongo import MongoClient
from gridfs import GridFS
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import DocumentForm
from django.core.urlresolvers import reverse

#added_self
from myproject.settings import PROJECT_DIR
from subprocess import call
import os
import shutil
from datetime import datetime
import pytz
from pytz import timezone
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required


if settings.DEBUG:
	@login_required(login_url='/login/go/')  #added after wards to ensure that files are not visible
	def serve_from_gridfs(request, path):
		# Serving GridFS files through Django is inefficient and
		# insecure. NEVER USE IN PRODUCTION!
		try:
			gridfile = gridfs_storage.open(path)
		except NoFile:
			# raise Http404
			return HttpResponse("<h1>Either file name is incorrect or file doesn't exist!</h1>")
		else:
			TEMP_DIR = os.path.join(PROJECT_DIR,'temp/')
			ORIG_FILE_DIR = os.path.join(PROJECT_DIR,'temp_orig/')

			

			#create TEMP_DIR is noy exists
			if not os.path.exists(TEMP_DIR):
				os.makedirs(TEMP_DIR)


			#emtying content of a TEMP_DIR folder
			# filelist = [ f for f in os.listdir(TEMP_DIR) ] #if f.endswith(".")
			# for f in filelist:
			# 	os.remove(f)

			#create ORIG_FILE_DIR if not exist
			if not os.path.exists(ORIG_FILE_DIR):
				os.makedirs(ORIG_FILE_DIR)
			
			

			ORIG_FILE = os.path.join(ORIG_FILE_DIR,gridfile.name);
						
			
			file_type = str(gridfile.name).split(".")[1]
			file_name = str(gridfile.name).split(".")[0]
			

			if file_type != 'pdf':  # for a particular file type
				do = open(ORIG_FILE,"ab")
				# print '++++++file name: '+ORIG_FILE
				#if file exists clear its content
				do.seek(0)
				do.truncate()
				do.write(gridfile.read())
				do.close()
				

				# print '+++++++++++++calling uno: '+ORIG_FILE
				call(["unoconv","-f","pdf","-o",TEMP_DIR,ORIG_FILE])
				# print '-------------uno called'
				os.remove(ORIG_FILE)
				shutil.rmtree(ORIG_FILE_DIR)
				# gridfile.close()

				
				# print '******output file:'+TEMP_DIR+file_name+'.pdf'
				name = file_name+'.pdf'
				# print 'llllllllllllllllll----filename: '+name
				PDF_DIR=os.path.join(TEMP_DIR,name)
				res = open(PDF_DIR,"rb")
			else:
				res = gridfile
				name = path
				# print 'xxxxxxxxxxxx;;;;;---'+path


			# do = open(ORIG_FILE,"ab")
			# print '++++++file name: '+ORIG_FILE
			# #if file exists clear its content
			# do.seek(0)
			# do.truncate()
			# do.write(gridfile.read())
			# do.close()
			# print '+++++++++++++calling uno: '+ORIG_FILE
			# call(["unoconv","-f","pdf","-o",TEMP_DIR,ORIG_FILE])
			# print '-------------uno called'
			# os.remove(ORIG_FILE)
			# shutil.rmtree(ORIG_FILE_DIR)
			# # gridfile.close()				
			# # print '******output file:'+TEMP_DIR+file_name+'.pdf'
			# name = file_name+'.pdf'
			# # print 'llllllllllllllllll----filename: '+name
			# PDF_DIR=os.path.join(TEMP_DIR,name)
			# res = open(PDF_DIR,"rb")

			return HttpResponse(res,mimetype=guess_type(name)[0]) #mimetype=guess_type(res)[0]

@login_required(login_url='/login/go/')
def download_file(request, path):
		# Serving GridFS files through Django is inefficient and
		# insecure. NEVER USE IN PRODUCTION!
		try:
			gridfile = gridfs_storage.open(path)
		except NoFile:
			# raise Http404
			return HttpResponse("<h1>Either file name is incorrect or file doesn't exist!</h1>")
		else:
			return HttpResponse(gridfile,mimetype=guess_type(path)[0]) 

@login_required(login_url='/login/go/')
def delete_file(request, path):
		# Serving GridFS files through Django is inefficient and
		# insecure. NEVER USE IN PRODUCTION!
		try:
			gridfile = gridfs_storage.delete(path)
			cl = MongoClient()
			db = cl.my_database
			db.gridfsuploads_userfiles.delete_one({'file_name':path})
		except NoFile:
			# raise Http404
			return HttpResponse("<h1>Either file name is incorrect or file doesn't exist!</h1>")
		else:
			return HttpResponseRedirect(reverse('file_uploading'))

@login_required(login_url='/login/go/')
def serve_files_list(request, *kwargs):
	usersession = request.session['name']
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		
		if form.is_valid():
			newfile = FileUpload(file = request.FILES['file'])
			newfile.save()
			# print newfile.file
			user_info = UserFiles(user = usersession, file_id = newfile.id, file_name = newfile.file)
			user_info.save()
			return HttpResponseRedirect(reverse('file_uploading'))

	else:
		form = DocumentForm()
	# url = reverse('list', kwargs={'username': classname})
	
	cl = MongoClient()
	db = cl.my_database #my_database - > database name
	# gd = GridFS(db,collection = 'storage')  #storage - > collection name in which files are stored
	# file_list = gd.list()
	# print file_list
	# file_list = FileUpload.objects.all()
	#added
	
	x = db.gridfsuploads_userfiles.find({'user':usersession}) #{'user':'anmol'}
	file_list = []
	for rec in x:
		# file_list[rec.get('file_name')]=rec.get('file_id')
		file_list.append(rec.get('file_name'))
	# print file_list
	return render_to_response(
		'gridfsuploads/fileupload_list.html',
		{'fileupload_list': file_list, 'form': form, 'usersession': usersession},
		context_instance=RequestContext(request)
	)

@login_required(login_url='/login/go/')
def clear_temp_dir(request,path):
	TEMP_DIR = os.path.join(PROJECT_DIR,'temp/')

	# emtying content of a TEMP_DIR folder is dir exists
	if os.path.exists(TEMP_DIR):
		shutil.rmtree(TEMP_DIR)
	# 	filelist = [ f for f in os.listdir(TEMP_DIR) ] #if f.endswith(".")
	# 	for f in filelist:
	# 		os.remove(f)
	
	return HttpResponse("<center><h4>Please wait...</h4></center>")

@login_required(login_url='/login/go/')
def file_properties(request,path):
	gridfile = gridfs_storage.open(path)
	file_type = str(gridfile.filename).split(".")[1]
	datetime_obj_naive = gridfile.upload_date

	date = datetime_obj_naive.replace(tzinfo=pytz.utc)

	# datetime_obj = gridfile.upload_date #datetime.strptime(gridfile.upload_date, "%Y-%m-%d %H:%M:%S")
	# datetime_obj_naive.utctimetuple()
	datetime_obj_india = date.astimezone(tz=timezone('Asia/Kolkata'))
	# print (datetime_obj_india)
	# datetime_obj_india = date.astimezone(pytz.utc)
	# date = pytz.utc.localize(datetime_obj_india)
	cl = MongoClient()
	db = cl.my_database
	x = db.gridfsuploads_userfiles.find_one({'file_name':path})



	properties = {"file_size":str(float(gridfile.length)/1000)+" KB","file_name":gridfile.filename,
	"file_type":file_type,"upload_date":datetime_obj_india, "owner":x.get("user")}

	return render_to_response(
		'gridfsuploads/file_properties.html',
		{'properties': properties},
		context_instance=RequestContext(request)
	)
@login_required(login_url='/login/go/')	
def logout(request):
	# print 'hello'
	logout(request)
	return HttpResponseRedirect('/login/go/')