from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create, name='click'),
    path('join/', views.join, name="join"),
    path('processing/', views.processing, name="processing"),
    path('signup/', views.SignUp.as_view(), name="register"),
    path('login/', views.Login, name = 'login'),
    path('Team/<int:pk>', views.ScurmProject, name = 'Project'),
    path('Team/<int:pk>/addTask', views.createTask, name = 'Add_Task'),
    path('DetailTask/<int:pk>', views.Detail_Task.as_view(), name = 'Detail_Task'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]