# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, RedirectView

from . import forms


@method_decorator(csrf_exempt, name='dispatch')
class Login(FormView):
    form_class = forms.LoginForm
    template_name = 'users/LoginTemplate.html'

    # def get(self, request, *args, **kwargs):
    #     form_instance = forms.LoginForm(data=request.GET)
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            next_url = self.request.GET.get('next', '/')
            if is_safe_url(next_url, settings.ALLOWED_HOSTS):
                messages.success(self.request, 'You`ve been loged in successfully!!!')
                return redirect(next_url)
            else:
                messages.error(self.request, 'This url is not safe!!!')
                return redirect('/')
        else:
            messages.error(self.request, 'User is not authenticated')
            return redirect('users:login')


class Logout(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You`ve been loged out successfully!!!')
        return redirect('PhoneBook:add-entry')


