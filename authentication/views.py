from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request,"authentication/index.html")



def signup(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            # Check if the username already exists
            user_exists = User.objects.filter(username=username).exists()

            if User.objects.filter(username=username):
                 messages.error(request,"Username already exists")
                 return redirect('signup')
            if User.objects.filter(email=email):
                 messages.error(request,"Email already exists")
                 return redirect('signup')
            if len(username)>10:
                 messages.error(request,"Username must be under 10 characters")
                 
            """if user_exists:
                messages.error(request, "Username already exists. Choose a different username.")
                return redirect('signup')"""

            # If the username doesn't exist, create a new user
            myuser = User.objects.create_user(username, email, password)
            myuser.save()

            messages.success(request, "Account successfully created")
            return redirect( 'signin')

        except IntegrityError as e:
            messages.error(request, "An error occurred while creating the account.")
            # You can log the exception for debugging purposes
            print(f"IntegrityError: {e}")

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            username=user.username
            return render(request,"authentication/index.html", {'username':username})

        else:
            messages.error(request,"bad credentials")
            return redirect('home')
            
    return render(request,"authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request,"logged out successfully!")
    return redirect('home')