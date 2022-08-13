from django.urls import path
from excel_sql.views import *

urlpatterns = [
    path("", index)
]
