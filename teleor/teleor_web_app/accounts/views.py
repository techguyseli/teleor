from django.contrib.auth import authenticate
from django.contrib.auth import login as loginn
from django.contrib.auth import logout as logoutt
from django.shortcuts import HttpResponse, render, redirect
from .forms import LoginForm


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'login/login.html') 

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login/login.html', {
            "message" : 'Il y avait un erreur, s\'il vous plait contacter l\'admin!',
            }) 
                                           

    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]
    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'login/login.html', {
            "message" : "Il n'existe aucun compte avec le nom d'utilisateur et/ou le mot de passe que vous avez entré!",
            })

    loginn(request, user)
    return redirect('index')

def logout(request):
    if request.user.is_authenticated:
        logoutt(request)
    return redirect('login')

