from django.shortcuts import render,redirect
from .models import*
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    blog = BlogPost.objects.all()
    context = {
        'blogs':blog
    }
    return render(request,'index.html',context)

@login_required(login_url='login_view')
def dashboard(request):
    
    return render(request,'dashboard.html',{'user_profile':UserProfile.objects.get(user = request.user)})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.warning(request,message="passwrod or username incorret")
            
    return render(request,'login_view.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.warning(request,'User already exists')
            elif User.objects.filter(email = email).exists():
                messages.warning(request,'email already exists')
            else:
                user = User.objects.create_user(username=username,password=password,email=email,is_staff = True)
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                messages.success(request,f'Congrats You are registerd Scuccesfully: username:{username} - password:{password}')
                user = authenticate(request, username = username,password = password)
                login(request,user)
                return redirect('dashboard')

        else:
            messages.warning(request,'passwrod not matched')

    return render(request,'signup_view.html')




def blog(request):
    blog = BlogPost.objects.all()
    context = {
        'blogs':blog
    }
    return render(request,'blog.html',context)

def contact(request):
    return render(request,'contact.html')


def logout_view(request):
    logout(request)
    return redirect('index')



@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user = request.user)
    if request.method == 'POST':
        user_profile.bio = request.POST.get('bio', '')
        profile_pic = request.FILES.get('profile_pic','')
        if profile_pic:
            user_profile.profile_pic = profile_pic
        user_profile.save()
        return redirect('dashboard')  # Redirect to dashboard after saving

    return render(request, 'edit_profile.html', {'user_profile': user_profile})