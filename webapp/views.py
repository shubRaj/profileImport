from django.contrib.auth.views import LoginView,TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
class Login(LoginView):
    template_name = "webapp/login.html"
class Home(TemplateView):
    template_name = "webapp/home.html"