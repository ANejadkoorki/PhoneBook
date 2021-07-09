# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView

from . import models


@method_decorator(csrf_exempt, name='dispatch')
class AddEntry(LoginRequiredMixin, CreateView):
    model = models.PhoneBook
    fields = (
        'first_name',
        'last_name',
        'phone_number',
    )
    template_name = 'PhoneBook/AddEntryTemplate.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name='PhoneBook/AddEntryTemplate.html')

    def form_invalid(self, form):
        return JsonResponse(data={
            'success': 'False',
            'error_message': 'Your Entry is Invalid Or Exists!!',
        }, status=400)

    def form_valid(self, form):
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
        if phone_number:
            if search_mode == 'exactly this number':
                Entries = self.queryset.filter(phone_number__exact=phone_number)
                if Entries:
                    return JsonResponse(data={
                        'success': 'True',
                        'success_message': 'Successfull! Number has been found',
                        'result_objects': list(Entries.values()),
                        'count': Entries.count()
                    }, status=201)
                else:
                    return JsonResponse(data={
                        'success': 'False',
                        'error_message': 'The Number not found!!!',
                    }, status=404)
            elif search_mode == 'starts with this number':
                Entries = self.queryset.filter(phone_number__startswith=phone_number)
                if Entries:
                    return JsonResponse(data={
                        'success': 'True',
                        'success_message': 'Successfull! Number has been found',
                        'result_objects': list(Entries.values()),
                        'count': Entries.count()
                    }, status=201)
                else:
                    return JsonResponse(data={
                        'success': 'False',
                        'error_message': 'The Number not found!!!',
                    }, status=404)
            elif search_mode == 'ends with this number':
                Entries = self.queryset.filter(phone_number__endswith=phone_number)
                if Entries:
                    return JsonResponse(data={
                        'success': 'True',
                        'success_message': 'Successfull! Number has been found',
                        'result_objects': list(Entries.values()),
                        'count': Entries.count()
                    }, status=201)
                else:
                    return JsonResponse(data={
                        'success': 'False',
                        'error_message': 'The Number not found!!!',
                    }, status=404)
            elif search_mode == 'contains this number':
                Entries = self.queryset.filter(phone_number__contains=phone_number)
                if Entries:
                    return JsonResponse(data={
                        'success': 'True',
                        'success_message': 'Successfull! Number has been found',
                        'result_objects': list(Entries.values()),
                        'count': Entries.count()
                    }, status=201)
                else:
                    return JsonResponse(data={
                        'success': 'False',
                        'error_message': 'The Number not found!!!',
                    }, status=404)
        return render(request, template_name='PhoneBook/SearchEntryTemplate.html')

#
