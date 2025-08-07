from django.shortcuts import render


def index(request):
    return render(request, 'auth_login.html')
# Create your views here.
