from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('users/register/', views.register, name='register'),
    path('users/login/', views.login_view, name='login_view'),
    path('users/change_account/', views.change_account, name='change_account'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('users/logout/', auth_views.LogoutView.as_view(template_name='Accounts/logout.html'), name="logout"),


]
