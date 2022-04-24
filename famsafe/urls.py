from django.urls import path
from . import views
from .views import (FileCreateView,)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('documentation', views.doc, name='doc'),
    path('terms-and-conditions', views.term, name='terms'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reg-dashboard/', views.reg_dash, name='reg-dash'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard-admin'),
    path('admin-files/', views.admin_files, name='admin-files'),
    path('admin-users/', views.admin_users, name='admin-users'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('upload/', FileCreateView.as_view(), name='upload'),
    path('delete/<int:pk>', views.delete_file, name='delete'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
