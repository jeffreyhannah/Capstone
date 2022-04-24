from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateUserForm, uploadForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, CreateView, DeleteView
#login requirement for specific page
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy





# Create your views here.
def index(request):
	return render(request, 'index.html')

def doc(request):
	return render(request, 'documentation.html')

def term(request):
	return render(request, 'terms.html')

def loginpage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('index')


#Dashboard page requiring login
#copy and paste below line for restricting pages
@login_required(login_url='login')
def dashboard(request):

	user_id = request.user


	queryset = uploadFile.objects.filter(user_id=user_id).order_by('-date_created')
	ordering = ['-date_posted']
	context = {
		"object_list": queryset
	}


	if request.user.is_staff:
		return redirect('dashboard-admin')
	else:
		return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def reg_dash(request):
	user_id = request.user


	queryset = uploadFile.objects.filter(user_id=user_id).order_by('-date_created')
	ordering = ['-date_posted']
	context = {
		"object_list": queryset
	}

	return render(request, 'dashboard.html', context)



#admin dashboard view
@login_required(login_url='login')
def dashboard_admin(request):
	model = User
	#all_users= get_user_model().objects.all().order_by('-date_joined')
	user_count = User.objects.all().count()
	ufiles = uploadFile.objects.all()
	file_count = uploadFile.objects.all().count()
	last_file = uploadFile.objects.last()
	context = {
		"file_list": ufiles,
		"users": user_count,
		"files": file_count,
		"lastfile": last_file,
	}

	if request.user.is_staff:
		return render(request, 'dash-admin.html', context)
	else:
		return redirect('dashboard')


#admin dashboard filelist
@login_required(login_url='login')
def admin_files(request):
	ufiles = uploadFile.objects.all()
	context = {
		"file_list": ufiles,

	}

	if request.user.is_staff:
		return render(request, 'admin-files.html', context)
	else:
		return redirect('dashboard')



#admin userlist
@login_required(login_url='login')
def admin_users(request):
	model = User
	#all_users= get_user_model().objects.all().order_by('-date_joined')
	all_users = User.objects.all().order_by('-last_login')
	context = {
		"user_list": all_users,

	}

	if request.user.is_staff:
		return render(request, 'admin-users.html', context)
	else:
		return redirect('dashboard')



#Register Function
def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		form = CreateUserForm()

		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				user.email = form.cleaned_data.get('email')
				messages.success(request,'Account was created for ' + user)
				return redirect('login')

	context = {'form': form}
	return render(request, 'register.html', context)


#Upload Function
class FileCreateView(LoginRequiredMixin, CreateView):
	model = uploadFile
	fields = [ 'file_field']

	template_name = 'upload.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
		if request.user.is_staff:
			return redirect('reg-dash')
		else:
			return redirect('dashboard')

#Delte-File Function
def delete_file(request,  pk):
	user_id = request.user.id
	queryset = uploadFile.objects.get(id=pk)
	if request.method == "POST":
		if queryset.user_id == user_id:
			queryset.delete()
			return redirect('dashboard')
		else:
			messages.info(request, 'You do not have premission to modify the file.')
			return redirect('index')
	context = {
		"item": queryset
	}
	return render(request, 'delete.html', context)
