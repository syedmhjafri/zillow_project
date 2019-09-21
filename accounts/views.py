from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST': # if POST, we know that it is the form submission
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # Check for username. User.objects -> .objects fetches the data from the database.
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already registered.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered.')
                    return redirect('register')
                else:
                    # Looks good.
                    user = User.objects.create_user(first_name=first_name,
                                                    last_name=last_name,
                                                    username=username,
                                                    email=email,
                                                    password=password)
                    # Login after registeration
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in.")
                    # return redirect('index')

                    # Saving a user and prompting the user to the login page to log in.
                    user.save()
                    messages.success(request, 'User successfully registered. Please login below.')
                    return redirect('login')


        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None: # 'is not None' checks if the user is in the database
            auth.login(request, user)
            messages.success(request, 'You are successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid user credentials. Please register.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You have been successfully logged out.")
    return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
