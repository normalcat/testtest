from django.shortcuts import render, HttpResponse, redirect
import bcrypt
import re
from models import *
from django.contrib import messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    all_users = user_reg.objects.all()
    data = {
        "all_users": all_users
    }
    return render(request,"resetful/index.html",data)

def new(request):
    return render(request,"resetful/new.html")

def edit(request,id):
    user = user_reg.objects.get(id=id)
    data = {
        "id": id,
        "single_user": user
    }
    return render(request,"resetful/edit.html",data)

def show(request,id):
    user = user_reg.objects.get(id=id)
    data = {
        "id": id,
        "single_user": user
    }
    return render(request,"resetful/show.html",data)
    #return HttpResponse("heee")

def create(request):
    if len(request.POST['first_name'])<=2:
        print request.POST['first_name']
        messages.add_message(request, messages.INFO, "First name should be longer than 2 characters\n")
        return redirect("/users/error",messages)
    if len(request.POST['last_name'])<=2:
        messages.add_message(request, messages.INFO, "Last name should be longer than 2 characters\n")
        return redirect("/users/error",messages)
    if not request.POST['first_name'].isalpha():
        messages.add_message(request, messages.INFO,"Fist name should not contain numbers\n")
        return redirect("/users/error",messages)
    if not request.POST['last_name'].isalpha():
        messages.add_message(request, messages.INFO,"Last name should not contain numbers\n")
        return redirect("/users/error",messages)
    if len(request.POST['password'])<8:
        messages.add_message(request, messages.INFO,"Password needs to be at least 8 chars\n")
        return redirect("/users/error",messages)
    if not request.POST['password']==request.POST['cpassword']:
        messages.add_message(request, messages.INFO,"Password does not match\n")
        return redirect("/users/error",messages)
    if len(request.POST['email'])<1:
        messages.add_message(request, messages.INFO,"Email cannot be blank\n")
        return redirect("/users/error",messages)
    elif not EMAIL_REGEX.match(request.POST['email']):
        messages.add_message(request, messages.INFO,"Invalid email address\n")
        return redirect("/users/error",messages)
    else:
        X = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        user_reg.objects.create(first_name = request.POST['first_name'],
                                last_name = request.POST['last_name'],
                                email = request.POST['email'].lower(),
                                password = X)
                              #  password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        # We'll then create a dictionary of data from the POST data received.
        return redirect('/users')

def destroy(request,id):
    x = user_reg.objects.get(id=id)
    x.delete()
    return redirect("/users")

def update(request):
    if request.POST['first_name']:
        print request.POST['first_name']
    if request.POST['last_name']:
        print request.POST['last_name']
    if request.POST['email']:
        print request.POST['email']
    x = user_reg.objects.get(id=request.POST['id'])
    x.first_name = request.POST['first_name']
    x.last_name = request.POST['last_name']
    x.email = request.POST['email']
    x.save()
    return redirect('/users')

def error(request):
    return render(request,"resetful/error.html")

def login(request):
    user=user_reg.objects.get(email=request.POST['email'])
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            user=user_reg.objects.get(email=request.POST['email'])
            data = {
                "single_user": user
            }
            render(request,"resetful/success.html",data)
        else:
            messages.add_message(request, messages.INFO,"Login fail\n")
            return redirect("/users/error")
    else:
        messages.add_message(request, messages.INFO,"Login fail\n")
        return redirect("/users/error")
    return render(request,"resetful/success.html",data)