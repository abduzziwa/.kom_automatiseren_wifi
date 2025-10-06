from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('setup/', views.setup_admin, name='setup'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('', views.dashboard, name='dashboard'),
    # path('add/', views.add_user, name='add_user'),
    # path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
