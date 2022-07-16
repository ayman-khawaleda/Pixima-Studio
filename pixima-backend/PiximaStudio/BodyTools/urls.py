from django.urls import path
from . import views
urlpatterns = [
    path('api-colorhair_tool',views.ColorHairToolView.as_view(),name='HairToolAPI')
]