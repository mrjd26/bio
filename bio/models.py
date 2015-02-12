from django.db import models

class Profile(models.Model):
  email = models.EmailField(primary_key=True)
  hometown = models.CharField(max_length=100, null=True)
  employer = models.CharField(max_length=100, null=True)
  college = models.CharField(max_length=100, null=True)
  color = models.CharField(max_length=100, null=True)
  hobby = models.CharField(max_length=100, null=True)

class Upload(models.Model):
  """ Database to handle avatar upload 
  
  Attributes
      is_avatar: the image currently being used as profile avatar
      url: the serving url of the image
  """
  image = models.ImageField(
                               upload_to = 'static',
                               blank = True,
                               null = True
                           )
  email = models.EmailField()
  is_avatar = models.BooleanField()
  url = models.CharField(max_length=255, primary_key=True)

class Verify(models.Model):
  """ db to store unique token on user registration
      and used subsequently to check during email confimation

  Attributes:
      token: A unique str created from the UUID module 
  """   
  email = models.EmailField(primary_key=True)
  token = models.CharField(max_length=255, null=True)

class Gallery(models.Model):
  """ Photo gallery upload model
  
  Attributes:
      blob_key: similar to a serving url, can be used with
      google blobstore, google cloud storage, and with the Images API etc.
      as an identifier 
  """
  image = models.ImageField(
                               upload_to = 'static',
                               blank = True,
                               null = True,
                           )
  email = models.EmailField()
  url = models.CharField(max_length = 255, primary_key = True)
  blob_key = models.CharField(max_length = 255)
  name = models.CharField(max_length = 255)
