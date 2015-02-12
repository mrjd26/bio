from django import forms
from models import Upload, Gallery

class UploadForm(forms.ModelForm):
  class Meta:
    model = Upload
    exclude = ['is_avatar', 'email', 'url']

class GalleryForm(forms.ModelForm):
  image = forms.ImageField(
                              widget = forms.FileInput(
                                  attrs={'id':'id_gallery'}
                              )
                          )

  class Meta:
    model = Gallery
    exclude = ['name', 'email', 'url', 'blob_key']
