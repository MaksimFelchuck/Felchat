from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from messenger.models import *
from main.views import get_black_list


# Create your views here.

@login_required()
def show_messages(request):
    messages = []
    for message in Message.objects.all():
        if message.user == request.user:
            messages.append(message)
    context = {
        "messages": messages
    }
    return render(request, "messages.html", context)


@login_required()
def write_message(request, username):
    if request.method == "POST":
        sended_message = request.POST.get("message")
        sended_message = Message(user=User.objects.get(username=username), \
                                 from_user=request.user, text_message=sended_message)
        sended_message.save()
        return redirect(f"/write/{username}")

    messages = []

    for message in Message.objects.all():
        if message in Message.objects.filter(user=request.user, from_user=User.objects.get(username=username)).order_by(
                "created") or \
                message in Message.objects.filter(user=User.objects.get(username=username),
                                                  from_user=request.user).order_by("created"):
            messages.append(message)
    messages.reverse()
    user_in_black_list, users_black_list = get_black_list(request.user.username)
    status = "Good"
    for black in users_black_list:
        if black.blocked_user.username == username:
            status = "You blocked this user"

    for black in user_in_black_list:
        if username == black.user.username:
            status = "You're been blocked by this user"

    context = {
        "messages": messages,
        "username": username,
        "status": status,
        "user_in_black_list": user_in_black_list,
        "users_black_list": users_black_list,
    }

    return render(request, "write_message.html", context)


@login_required()
def block(request, username):
    block_user = BlackList(user=request.user, blocked_user=User.objects.get(username=username))
    block_user.save()
    return redirect('/')


@login_required()
def unblock(request, username):
    block_user = BlackList.objects.get(user=request.user, blocked_user=User.objects.get(username=username))
    block_user.delete()
    return redirect(f'/write/{username}')
