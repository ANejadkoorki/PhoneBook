# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView

from . import models, forms


@method_decorator(csrf_exempt, name='dispatch')
class AddEntry(LoginRequiredMixin, CreateView):
    model = models.PhoneBook
    form_class = forms.AddEntryForm
    template_name = 'PhoneBook/AddEntryTemplate.html'
    extra_context = dict()

    # def get(self, request, *args, **kwargs):
    #     return render(request, template_name='PhoneBook/AddEntryTemplate.html')

    def form_invalid(self, form):
        return JsonResponse(data={
            'success': 'False',
            'error_message': 'Your Entry is Invalid Or Exists!!',
        }, status=400)

    def form_valid(self, form):
        form.instance.creator = self.request.user  # we can access to users like this
        form.save()
        return JsonResponse(data={
            'success': 'True',
            'success_message': 'The Entry Was Created Successfully',
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class SerarchEntry(LoginRequiredMixin, ListView):
    model = models.PhoneBook
    queryset = model.objects

    # ask question about how to access to queryset`s string object
    def get(self, request, *args, **kwargs):
        phone_number = request.GET.get('phone_number')
        search_mode = request.GET.get('search_mode')
        entries = None
        if phone_number:
            if search_mode == 'exactly this number':
                entries = self.queryset.filter(phone_number__exact=phone_number, creator=self.request.user)
            elif search_mode == 'starts with this number':
                entries = self.queryset.filter(phone_number__startswith=phone_number, creator=self.request.user)
            elif search_mode == 'ends with this number':
                entries = self.queryset.filter(phone_number__endswith=phone_number, creator=self.request.user)
            elif search_mode == 'contains this number':
                entries = self.queryset.filter(phone_number__contains=phone_number, creator=self.request.user)
            if entries:
                return JsonResponse(data={
                    'success': 'True',
                    'success_message': 'Successfull! Number has been found',
                    'result_objects': list(entries.values()),
                    'count': entries.count(),
                }, status=201)
            else:
                return JsonResponse(data={
                    'success': 'False',
                    'error_message': 'The Number not found!!!',
                }, status=404)
        return render(request, template_name='PhoneBook/SearchEntryTemplate.html')


class Contacts(LoginRequiredMixin, ListView):
    model = models.PhoneBook
    template_name = 'PhoneBook/contactsTemplate.html'
    paginate_by = 5

    def get_queryset(self):
        query_set = models.PhoneBook.objects.filter(creator=self.request.user)
        return query_set


class EditEntry(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = models.PhoneBook
    fields = (
        'first_name',
        'last_name',
        'phone_number',
        'id'
    )
    success_message = 'Your Entry Has been Updated Successfully!!! '
    success_url = reverse_lazy('PhoneBook:contacts')
    template_name = 'PhoneBook/editEntryTemplate.html'

    def form_invalid(self, form):
        pk = self.get_object().id
        messages.error(self.request, 'Please Edit Your Entry Correctly!!!')
        return redirect('PhoneBook:edit-entry', pk)
