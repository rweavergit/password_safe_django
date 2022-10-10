from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.db.models import Q
from .forms import RegisterForm, LoginForm

# Render home screen as default
def home_page(request):
      return render(request, 'pw_storage/home.html')

def register_page(request):
      # Use the Registration form from forms.py
      form = RegisterForm(request.POST or None)
      if request.user.is_authenticated:
            messages.success(request, "You are already logged in as %s " % request.user + " you can't register or login ones already logged in!")
            return redirect(home_page)

      if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            try:
                  user = User.objects.create_user(username, email, password)
            except: 
                  user = None
            if user != None:
                  login(request, user)
                  return redirect(user_pw_all)
            else:
                  request.session['register_error'] = 1 # 1 == True
      return render(request, 'pw_storage/user_account/register.html', {"form": form})

def login_page(request):
      form = LoginForm(request.POST or None)
      if request.user.is_authenticated:
            messages.success(request, "You are already logged in as %s" % request.user + " you can't register or login ones already logged in!")
            return redirect(home_page)
      if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user != None:
                  login(request, user)
                  return redirect(user_pw_all)
            else:
                  messages.warning(request, 'Please enter the right password!')
      return render(request, "pw_storage/user_account/login.html", {"form": form})

@login_required(login_url=login_page)
def logged_out_page(request):
      logout(request)
      return render(request, "pw_storage/user_account/logged_out.html")
