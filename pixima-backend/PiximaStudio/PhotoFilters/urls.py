from django.urls import path
from . import views

urlpatterns = [
    path(
        "api-glitch_filter",
        view=views.GlitchFilterView.as_view(),
        name="GlitchFilterAPI",
    ),
    path(
        "api-circle_filter",
        view=views.CircleFilterView.as_view(),
        name="CircleFilterAPI",
    ),
]
