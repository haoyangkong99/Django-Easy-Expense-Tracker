from django.shortcuts import render,redirect


from django.contrib import messages
from django import forms
from django.contrib.auth import login
from django.contrib.auth.models import User, auth

def register(request):
    return render(request,'register.html')

def doRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password==confirmpassword:
            if User.objects.filter(email=email).exists():
                print("error")
                messages.info(request, 'This email already exists')
                return redirect(register)
            else:
                user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
                user.save()
                user_login=auth.authenticate(email=email, password=password)
                auth.login(request, user_login)
                return redirect("index")

        else:
            return redirect(register)
    else:
        return redirect(register)
def login(request):
    return render(request,'login.html')
def doLogin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user=User.objects.filter(email=email).first()

        user = auth.authenticate(username=user.username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect(login)

    else:
        return redirect(login)



def forgetPass(request):
    return render(request,"forgot-password.html")

def logout(request):
    auth.logout(request)
    return redirect(login)