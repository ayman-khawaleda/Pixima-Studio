from django.urls import path
from . import views
urlpatterns = [
    path('api-crop_tool',view=views.CropToolView.as_view(),name='CropToolAPI'),
    path('api-flip_tool',view=views.FlipToolView.as_view(),name='FlipToolAPI'),
    path('api-rotate_tool',view=views.RotateToolView.as_view(),name='RotateToolAPI'),
    path('api-resize_tool',view=views.ResizeToolView.as_view(),name='ResizeToolAPI'),
    path('api-contrast_tool',view=views.ContrastToolView.as_view(),name='ContrastToolAPI'),
    path('api-saturation_tool',view=views.SaturationToolView.as_view(),name='SaturationToolAPI'),
    path('api-changecolor_tool',view=views.ChangeColorToolView.as_view(),name='ChangeColorToolAPI'),
]