from django.contrib.auth.views import LoginView,TemplateView,LogoutView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
class Login(UserPassesTestMixin,LoginView):
    template_name = "webapp/login.html"
    def test_func(self):
        return not self.request.user.is_authenticated
    def handle_no_permission(self):
        return redirect("app_webapp:home")
class Home(LoginRequiredMixin,TemplateView):
    template_name = "webapp/home.html"
class Logout(LoginRequiredMixin,LogoutView):
    pass