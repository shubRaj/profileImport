from typing import List
from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.views.generic import ListView
from .models import CSVModel
class Login(UserPassesTestMixin,LoginView):
    template_name = "webapp/login.html"
    def test_func(self):
        return not self.request.user.is_authenticated
    def handle_no_permission(self):
        return redirect("app_webapp:home")
class Home(LoginRequiredMixin,ListView):
    template_name = "webapp/home.html"
    context_object_name = "csvs"
    def get_queryset(self):
        return CSVModel.objects.all()
class Logout(LoginRequiredMixin,LogoutView):
    pass
# def handleFile