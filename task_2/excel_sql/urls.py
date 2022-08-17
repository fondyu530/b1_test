from django.urls import path
from .views import *

urlpatterns = [
    path("", upload_file, name="main"),
    path("display/<str:file_name>", display_file)
]
