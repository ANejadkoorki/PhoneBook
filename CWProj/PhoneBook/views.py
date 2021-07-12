# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
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


class EditEntry(UpdateView):
    model = models.PhoneBook
    fields = (
        'first_name',
        'last_name',
        'phone_number',
    )
    success_url = reverse_lazy('firstApp:posts')
    template_name = 'PhoneBook/AddEntryTemplate.html'
