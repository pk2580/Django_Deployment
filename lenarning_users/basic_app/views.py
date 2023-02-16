from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


# log in
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import  login_required



# Create your views here.
# Registration
def index(request):
    return render(request,'basic_app/index.html')


def register(request):

    registered= False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)


        # here we are validating and both forms and graving the data from forms
        # hashing the password and saving in databases

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()


            profile=profile_form.save(commit=False)


            # thsi define the onetooe relationship with model ie user=user
            profile.user= user


            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered= True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

     # here we create a 3 keys which are user_form,profile_form and registered which are inject in regis.html
    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

# login in and log out

@login_required
def special(request):
    return HttpResponse("You are logiged in , Nice!")



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)
        # django automate authenticate the username and password in existing db

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Accont is not active")

        else:
            print("Some tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse()

    else:
         return render(request,'basic_app/login.html',{})
