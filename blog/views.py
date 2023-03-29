from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import HttpResponse
from .filters import PostFilter
from .forms import CommentForm,CreateUserForm,ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'blog/register.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'blog/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def PostList(request):
	search= request.GET.get('search')
	category = request.GET.get('category')
	
	if category == None:
		posts=Post.objects.filter(status=1)		
	else:	
		posts = Post.objects.filter(category__name=category)					

	
	categories= Category.objects.all()
	#Paginator
	page = request.GET.get('page')
	paginator=Paginator(posts, 6)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)


	context={'posts':posts, 'categories':categories }
	return render(request, 'blog/index.html', context)


def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    total_comment=comments.count()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect('detail', post.slug)
    else:
        form = CommentForm()

    context={'post':post, 'comments':comments, 'new_comment':new_comment, 'form':form, 'total_comment':total_comment} 
    return render(request, 'blog/detail.html', context)   



@login_required(login_url='login')
def accountSettings(request):
	profile = request.user.profile
	form=ProfileForm(instance=profile)

	if request.method == 'POST':
		form=ProfileForm(request.POST, request.FILES,instance=profile)
		if form.is_valid():
			form.save()


	context={'form':form, 'profile':profile}
	return render(request, 'blog/settings.html', context) 


    
