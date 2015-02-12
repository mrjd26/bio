from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from base64 import b64decode
from models import Gallery
from forms import GalleryForm
import json
import cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url
from google.appengine.api import images

bucket_name = 'pg987'

@login_required
def gallery_uploader(request):
  """
  uploads image to google cloud storage
  stores some metadata in DB

  Args: None
  Returns: None
  """  
  email = request.user.email

  if request.method == 'POST':
    imageupload = GalleryForm(request.POST, request.FILES)
    if imageupload.is_valid():
      u = imageupload.save(commit=False)

      uploaded_file = request.FILES['image']
      content_type = request.FILES['image'].content_type
      name = request.FILES['image'].name
      
      data = uploaded_file.read()
     
      gcs_file = gcs.open(
                             ('/' + bucket_name + '/' + name),
                             mode = 'w',
                             content_type = content_type,
                             options = { 
                               'x-goog-acl': 'bucket-owner-full-control'
                             }
                         )
      gcs_file.write(data)
      gcs_file.close()

      #get_serving_url
      blob_key = blobstore.create_gs_key(
                                  '/gs/' + bucket_name + '/' + name
                                        )
      serving_url = get_serving_url(blob_key)

      #save user uploaded photo info in Gallery Database
      g = Gallery(
                     blob_key = blob_key,
                     url = serving_url,
                     email = email,
                     name = name,
                 )
      g.save()
  return HttpResponseRedirect('/my_account/')

@login_required
def thumbnailer(request):
  """
  finds users gallery photos

  Args: None
  Returns:
      List of serving Urls
  """

  output = {}
  output['urls'] = []

  email = request.user.email
  #lookup user in Gallery if exists
  g = Gallery.objects.filter(email = email)
  
  if len(g) == 0:
    response = []
  else:
    for photo in g:

      """
      ***saving for later ****
      stats = gcs.stat('/' + bucket_name + '/' + photo.name)
      img = images.Image(blob_key = photo.blob_key)
      img.resize(width=200, height=200)
      img.im_feeling_lucky()
      thumbnail = img.execute_transforms(output_encoding=images.JPEG)
      output.append(thumbnail)
      """
      serving_url = photo.url
      output['urls'].append(serving_url)

    response = json.dumps(output)

  return HttpResponse(response)

@csrf_exempt
def b64_binary(request):

  """saving for later"""

  base64 = request.body
  
  first_comma = base64.find(",")
  data = base64[first_comma+1:]
  binary = b64decode(data)

  gcs_file = gcs.open(
   ('/pg987/' + 'name'),
   mode = 'w',
   options = {
     'x-goog-acl': 'bucket-owner-full-control'
   }
  )
  
  gcs_file.write(binary.encode('utf-8'))
  gcs_file.close()
  
  return HttpResponse(name)
