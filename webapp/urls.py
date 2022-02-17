from urllib.parse import urlparse
from django.urls import path
from . import views
app_name = "app_webapp"
urlpatterns = [
    path("login/",views.login,name="login"),
    path("",views.home,name="home"),
]