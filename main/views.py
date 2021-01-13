from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.forms import *
from main.filters import UserFilter
from messenger.models import *


# Create your views here.

def get_black_list(user):
    black_list = BlackList.objects.all()
    users_black_list = []
    for black in black_list:
        if (black.blocked_user.username != user) and \
                (black.user.username == user):
            users_black_list.append(black)
    user_in_black_list = []
    for black in black_list:
        if black.blocked_user.username == user:
            user_in_black_list.append(black)
    return user_in_black_list, users_black_list


@login_required()
def main(request):
    users = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=users)
    users = user_filter.qs
    user_in_black_list, users_black_list = get_black_list(request.user.username)
    context = {
        "user_filter": user_filter,
        "users": users,
        "user_in_black_list": user_in_black_list,
        "users_black_list": users_black_list
    }
    return render(request, "home.html", context)


@login_required()
def log_out(request):
    logout(request)
    return redirect("/")


def log_in(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/")

    else:

        return render(request, "accounts/login.html")


def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            return render(request, "accounts/registration.html", {"form": form})

    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = UserForm()
        context = {
            "form": form
        }
        return render(request, "accounts/registration.html", context)
