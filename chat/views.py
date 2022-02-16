from django.shortcuts import render, redirect
from chat.forms import JoinForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

"""
Create a non-admin user.
"""
def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB.
            user = join_form.save()
            # Encrypt the password.
            user.set_password(user.password)
            # Save encrypted password to DB.
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console.
            page_data = { "join_form": join_form }
            return render(request, 'slaykcord/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'slaykcord/join.html', page_data)

"""
Log in as a non-admin user.
"""
def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # Get the username and password.
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                # Is the account active?
                if user.is_active:
                    login(request,user)
                    # Send user home.
                    return redirect("/")
                else:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'slaykcord/login.html', {"login_form": LoginForm})
    else:
        # Nothing provided for username and/or password.
        return render(request, 'slaykcord/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")

"""
Home page.
"""
@login_required(login_url='/login/')
def index(request):
    # Alphabetically display rooms.
    rooms = Room.objects.order_by("title")
    return render(request, "index.html", {
        "rooms": rooms,
    })
