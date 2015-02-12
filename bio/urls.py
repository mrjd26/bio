from django.conf.urls import patterns, include, url

from bio import views, helper_view

urlpatterns = patterns('',
  url(r'^$', views.user_bio),
  url(r'delete/$', views.delete),
  url(r'save/$', views.save),

  url(r'gallery/$', helper_view.gallery_uploader),
  url(r'thumbnail/$', helper_view.thumbnailer),

  url(r'binary_upload/$', helper_view.b64_binary),

)
