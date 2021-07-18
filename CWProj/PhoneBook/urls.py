from django.urls import path

from . import views

app_name = 'PhoneBook'

urlpatterns = [
    path('AddEntry/', views.AddEntry.as_view(), name='add-entry'),
    path('SearchEntry/', views.SerarchEntry.as_view(), name='search-entry'),
    path('Contacts/', views.Contacts.as_view(), name='contacts'),
    path('EditEntry/<int:pk>', views.EditEntry.as_view(), name='edit-entry'),
    path('Activities/', views.ActivitiesHistory.as_view(), name='activities')
]
