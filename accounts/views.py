from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from EmailAuthSystem import settings
from django.core.mail import send_mail

# Create your views here.
def index(request):
    User.objects.all().delete()
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if User.objects.filter(username=username):
            messages.error(request,"Username already exist!... Try another one")
            return redirect('signup')
        
        if len(username)>15:
            messages.error(request,"Username must be under 15 character..")
            return redirect("signup")
        
        if password1!=password2:
            messages.error(request,"Password did't match!")
            return redirect("signup")


        #Creating the User
        myuser=User.objects.create_user(username=username,email=email,password=password1)
        myuser.save()
        messages.success(request,"Your Accounf has been created successfully.  ")

        #welcome Email
        subject="Welcome to Shyam's - EmailAuthSystem"
        message=f"Hello {myuser.username} ! \n Welcome to Shyam's Email Authentication System \n Thankyou for visitng our website😊👋🙏🙏"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=False)
        return redirect("signin")
    
    return render(request,"authentication/signup.html")
 
def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        #Cheking user if exist or not
        user= authenticate(username=username,password=password)
        if user  is not None:
            login(request,user)
            messages.success(request,"Login Sussessful")
            return render(request,"home.html")
        else:
            messages.error(request,"Credential not matched... Try Again")
            return redirect("signin")
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Successully logout.")
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # this iterates and clears the messages
    return redirect('index')