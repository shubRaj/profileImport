from urllib.parse import urlparse
from django.urls import path
from . import views
app_name = "app_webapp"
urlpatterns = [
    path("login/",views.Login.as_view(),name="login"),
    path("",views.Home.as_view(),name="home"),
]