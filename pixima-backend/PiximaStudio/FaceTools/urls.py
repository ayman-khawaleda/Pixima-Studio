from django.urls import path
from . import views
urlpatterns = [
    path("api-coloreyes_tool",view=views.EyesColorToolView.as_view(),name="ColorEyesToolAPI"),
    path("api-resizeeyes_tool",view=views.EyesResizeToolView.as_view(),name="ResizeEyesToolAPI"),
]