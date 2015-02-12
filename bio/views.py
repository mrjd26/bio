from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import Profile, Upload
from emailusernames.utils import get_user
from forms import UploadForm, GalleryForm
from django.contrib.auth.decorators import login_required
import json
from django.template import RequestContext

import cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url

bucket_name = 'pg987'

@login_required
def user_bio(request):
  """
  'my_account' view used to handle avatar image upload
  and routing and templating of users account
  Args: None
  Returns:
      form for avatar upload
  """
  email = request.user.email

  if request.method == 'POST':
    imageupload = UploadForm(request.POST, request.FILES)
    
    if imageupload.is_valid():

      u = imageupload.save(commit=False)
      #image upload to google cloud storage
      uploaded_file = request.FILES['image']
      content_type = request.FILES['image'].content_type
      name = request.FILES['image'].name
      
      data = uploaded_file.read()  
      gcs_file = gcs.open(
                             ('/' + bucket_name + '/' + name),
                             mode = 'w',
                             content_type = 'image/jpeg',
                             options = {
                               'x-goog-acl': 'bucket-owner-full-control'
                             }
                         )
      gcs_file.write(data)
      gcs_file.close()

      #get_serving_url from google and stats
      #avatar = gcs.open('/' + bucket_name + '/' + name)
      blob_key = blobstore.create_gs_key(
                                          '/gs/' + bucket_name + '/' + name
                                        )
      serving_url = get_serving_url(blob_key)
      
      #find existing avatar image
      try:
        u = Upload.objects.get(email = email, is_avatar = True)
      except Upload.DoesNotExist:
        u = False

      #set is_avatar to False but keep entry in db
      if u:
        u.is_avatar = False
        u.save()

      #insert the uploaded avatar
      u = Upload(url = serving_url, email = email, is_avatar = True)
      u.save() 
      stats = gcs.stat('/' + bucket_name + '/' + name)
    
      return HttpResponseRedirect('/my_account/')

  else:
    form = UploadForm()
    gallery_form = GalleryForm()

    try:
      u = Upload.objects.get(email = email, is_avatar = True)
      serving_url = u.url
    except Upload.DoesNotExist:
      serving_url = '/static/bio/blank.png'
      
  return render_to_response(
                               'profile.html',
                               {
                                   'form': form,
                                   'gallery_form': gallery_form,
                                   'serving_url': serving_url,
                                   'user': email,
                               },
                               context_instance = RequestContext(request)
                           )

@login_required
def delete(request):
  """
  GET
  removes an entry in the database (sets data to NULL) 
  Params:
      the 'element' from the HTML form
  Returns:
      updated JSON dictionary 
  """
  user = request.user.email
  #return fiele to NULL for element
  b = Profile.objects.get(email = user)
  element = request.GET['element']
  setattr(b, element, None)
  b.save()

  #database to JSON
  b = Profile.objects.filter(email = user).values()
  db_data = b[0]
  data = json.dumps(db_data)

  return HttpResponse(data)

@login_required
def save(request):
  """
  GET 
  updates the users database with their profile information
  Params: 
      HTML form - included in request as query string
  Returns:
      JSON dictionary of form...
      *empty strings for incomplete fields
  """
  user = request.user.email

  #find logged in users Profile
  try:
    b = Profile.objects.filter(email = user).values()
    db_data = b[0]

  #create new Profile if none exists for user
  except (Profile.DoesNotExist, IndexError) as e:
    b = Profile(email=user)
    b.save()

  #update database with new field values
  if db_data:
    querydict_form = request.GET
    python_data = dict(querydict_form.iterlists())
    try:
      del python_data['csrfmiddlewaretoken']
    except KeyError:
      pass

    for form_key, form_value in python_data.iteritems():
        #compare the form to the database
        if len(form_value[0]) > 0 and \
        db_data[form_key] == None:
          #update field in database
          b = Profile.objects.get(email = user)
          setattr(b, form_key, form_value[0])
          b.save()
          db_data[form_key] = form_value[0]
        #remove the queryset value list brackets
        python_data[form_key] = form_value[0]

    data = json.dumps(db_data)

  return HttpResponse(data)
