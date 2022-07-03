from django.urls import path
from . import views

urlpatterns = [
    path('',view=views.Index.as_view(),name='Index'),
    path('api-upload_image',view=views.UploadImage.as_view(),name='UploadImageAPI')
]