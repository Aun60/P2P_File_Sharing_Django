from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send/", views.send_file_view, name="send_file"),
    path("file/<str:filename>/", views.file_content_view, name="file_content"),
]

