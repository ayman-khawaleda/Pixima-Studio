from django.urls import path
from . import views
urlpatterns = [
    path('api-crop_tool',view=views.CropToolView.as_view(),name='CropImageAPI'),
]