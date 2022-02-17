from django.shortcuts import render
def login(request):
    return render(request,"webapp/login.html")
def home(request):
    return render(request,"webapp/home.html")