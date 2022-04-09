from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateUserForm, uploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, CreateView, DeleteView
#login requirement for specific page
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model





# Create your views here.
def index(request):
	return render(request, 'index.html')

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
	User = get_user_model()
	lusers = User.objects.values()
	ufiles = uploadFile.objects.all()
	queryset = uploadFile.objects.filter(user_id=user_id).order_by('-date_created')
	ordering = ['-date_posted']
	context = {
		"object_list": queryset
	}
	contextuf = {
		"user_list": lusers,
		"file_list": ufiles
	}



	if request.user.is_superuser:
		return render(request, 'dash-admin.html', contextuf)
	else:
		return render(request, 'dashboard.html', context)


#admin dashboard view
@login_required(login_url='login')
def dashboard_admin(request):
	if request.user.is_superuser:
		return render(request, 'dash-admin.html')
	else:
		return redirect('dashboard.html')


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
		return redirect('dashboard')


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
