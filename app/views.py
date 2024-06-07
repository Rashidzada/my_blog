from django.shortcuts import render,redirect
from .models import*
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):

    blog = BlogPost.objects.filter(status = 'accepted')
    context = {
        'blogs':blog
    }
    return render(request,'index.html',context)

@login_required(login_url='login_view')
def dashboard(request):
    user_posts = BlogPost.objects.filter(author = request.user).order_by('-id')
    context = {
        'posts':user_posts,
        'user_profile':UserProfile.objects.get(user = request.user)
    }
    return render(request,'dashboard.html',context)


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
                return redirect('edit_profile')

        else:
            messages.warning(request,'passwrod not matched')

    return render(request,'signup_view.html')




def blog(request):
    query = request.POST.get('q')
    if query:
        posts = BlogPost.objects.filter(title__icontains=query)
    else:
        posts = BlogPost.objects.filter(status = 'accepted').order_by('-id')
    
    context = {'posts': posts, 'query': query}
    return render(request, 'blog.html', context)


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(name = request.POST['name'],email = request.POST['email'],subject = request.POST['subject'],message = request.POST['message'])
        messages.success(request,'Thank You to contact us we soon will be responsed .')
        return redirect('index')
    return render(request,'contact.html')


def logout_view(request):
    logout(request)
    return redirect('index')



@login_required(login_url='login_view')
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


def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        youtube_link = request.POST['youtube_link']
        BlogPost.objects.create(author = request.user ,title = title , content = content , image = image,youtube_link = youtube_link)
        messages.success(request,'Your Post Created Successfully')
        return redirect('dashboard')
    return render(request,'create_post.html')

def view_post(request,post_id):
    post = BlogPost.objects.get(id = post_id)
    user_profile = UserProfile.objects.get(user = post.author)

    context = {
        'post':post,
        'user_profile':user_profile,
    }
    return render(request,'view_post.html',context)

def edit_post(request,post_id):
    post = BlogPost.objects.get(id = post_id)
    if request.method == "POST":
        post.title = request.POST.get('title','')
        post.content = request.POST.get('content','')
        image = request.FILES.get('image','')
        post.youtube_link = request.POST.get('youtube_link','')
        if image:
            post.image = image
        post.save()
        messages.success(request,'Your Post Updated Successfully')
        return redirect('dashboard')
    
    return render(request,'edit_post.html',{'post':post})


def delete_post(request,post_id):
    post = BlogPost.objects.get(id = post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Your Post Deleted Successfully')
        return redirect('dashboard')
        
    return render(request,'delete_post.html',{'post':BlogPost.objects.get(title = post.title)})