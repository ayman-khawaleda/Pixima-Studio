from django.urls import path
from . import views
urlpatterns = [
    path('api-crop_tool',view=views.CropToolView.as_view(),name='CropToolAPI'),
    path('api-flip_tool',view=views.FlipToolView.as_view(),name='FlipToolAPI'),
    path('api-rotate_tool',view=views.RotateToolView.as_view(),name='RotateToolAPI')
]