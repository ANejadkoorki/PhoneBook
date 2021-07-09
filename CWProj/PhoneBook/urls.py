from django.urls import path

from . import views

app_name = 'PhoneBook'

urlpatterns = [
    path('AddEntry/', views.AddEntry.as_view(), name='add-entry'),
    path('SearchEntry/', views.SerarchEntry.as_view(), name='search-entry'),
]
