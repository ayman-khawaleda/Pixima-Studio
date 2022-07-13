from django.urls import path
from . import views
urlpatterns = [
    path("api-coloreyes_tool",view=views.EyesColorToolView.as_view(),name="ColorEyesToolAPI"),
    path("api-resizeeyes_tool",view=views.EyesResizeToolView.as_view(),name="ResizeEyesToolAPI"),
    path("api-resizenose_tool",view=views.NoseResizeToolView.as_view(),name="ResizeNoseToolAPI"),
    path("api-smoothface_tool",view=views.SmoothFaceToolView.as_view(),name="SmoothFaceToolAPI"),
    path("api-whiteteeth_tool",view=views.WhiteTeethToolView.as_view(),name="WhiteTeethToolAPI"),
]