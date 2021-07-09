from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('Login/', views.Login.as_view(), name='login'),
    path('Logout/', views.Logout.as_view(), name='logout')
]
