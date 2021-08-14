# Create your views here.
import weasyprint
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.utils.translation import ugettext as _
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from . import models, forms, serializers


@method_decorator(csrf_exempt, name='dispatch')
class AddEntry(LoginRequiredMixin, CreateView):
    model = models.PhoneBook
    form_class = forms.AddEntryForm
    template_name = 'PhoneBook/AddEntryTemplate.html'

    def get(self, request, *args, **kwargs):
        self.request.session['activities'].update({str(timezone.now()): _('visiting Add Entry page')})
        self.request.session.save()
        return render(request, template_name='PhoneBook/AddEntryTemplate.html')

    def form_invalid(self, form):
        self.request.session['activities'].update(
            {str(timezone.now()): _('trying to add an entry but it was invalid.')})
        self.request.session.save()
        return JsonResponse(data={
            'success': 'False',
            'error_message': _('Your Entry is Invalid Or Exists!!'),
        }, status=400)

    def form_valid(self, form):
        form.instance.creator = self.request.user  # we can access to users like this
        form.save()
        self.request.session['activities'].update({str(timezone.now()): _('An entry was added.')})
        self.request.session.save()
        return JsonResponse(data={
            'success': 'True',
            'success_message': _('The Entry Was Created Successfully'),
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
                self.request.session['activities'].update({str(timezone.now()): _('searched in entries.')})
                self.request.session.save()
                return JsonResponse(data={
                    'success': 'True',
                    'success_message': _('Successfull! Number has been found'),
                    'result_objects': list(entries.values()),
                    'count': entries.count(),
                }, status=201)
            else:
                self.request.session['activities'].update(
                    {str(timezone.now()): _('searched in entries but unsuccessful.')})
                self.request.session.save()
                return JsonResponse(data={
                    'success': 'False',
                    'error_message': _('The Number not found!!!'),
                }, status=404)
        self.request.session['activities'].update({str(timezone.now()): _('visited search entry page.')})
        self.request.session.save()
        return render(request, template_name='PhoneBook/SearchEntryTemplate.html')


class Contacts(LoginRequiredMixin, ListView):
    model = models.PhoneBook
    template_name = 'PhoneBook/contactsTemplate.html'

    def get(self, request, *args, **kwargs):
        self.request.session['activities'].update({str(timezone.now()): _('visited contacts page.')})
        self.request.session.save()
        qs = self.get_queryset()
        paginated = Paginator(qs, 8)
        paginated_page = paginated.get_page(request.GET.get('page', 1))
        return render(
            request,
            template_name='PhoneBook/contactsTemplate.html',
            context={
                'object_list': paginated_page,
                'page_obj': paginated,
            })

    def get_queryset(self):
        query_set = models.PhoneBook.objects.filter(creator=self.request.user)
        return query_set


class ContactsPdf(LoginRequiredMixin, ListView):
    """
        this view used to get pdf of contacts
    """
    model = models.PhoneBook
    template_name = 'PhoneBook/contactsPDF.html'

    def get_queryset(self):
        qs = self.model.objects.filter(creator=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        normal_rendered_page = super(ContactsPdf, self).get(request, *args, **kwargs)

        rendered_content = normal_rendered_page.rendered_content

        pdf = weasyprint.HTML(string=rendered_content, base_url='http://127.0.0.1:8000').write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        return response


class EditEntry(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = models.PhoneBook
    fields = (
        'first_name',
        'last_name',
        'phone_number',
        'id'
    )
    template_name = 'PhoneBook/editEntryTemplate.html'
    success_message = _('Your Entry Has been Updated Successfully!!! ')
    success_url = reverse_lazy('PhoneBook:contacts')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.session['activities'].update({str(timezone.now()): _('visited Edit Entry page.')})
        self.request.session.save()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        self.request.session['activities'].update({str(timezone.now()): _('Edited An Entry.')})
        self.request.session.save()
        messages.success(self.request, _('Your Entry Has been Updated Successfully!!!'))
        return redirect('PhoneBook:contacts')

    def form_invalid(self, form):
        self.request.session['activities'].update({str(timezone.now()): _('Editing Entry was unsuccessful.')})
        self.request.session.save()
        pk = self.get_object().id
        messages.error(self.request, _('Please Edit Your Entry Correctly!!!'))

        return redirect('PhoneBook:edit-entry', pk)


class ActivitiesHistory(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        history = []
        self.request.session['activities'].update({str(timezone.now()): _('visited history page.')})
        self.request.session.save()
        ###############
        for i in range(5):
            try:
                history.append(self.request.session['activities'].popitem())
                print(history)
            except:
                break
        print(history)
        return render(request, 'PhoneBook/historyTemplate.html', context={
            'history': history
        })


"""
    DRF
"""


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PhoneBookViewSet(ModelViewSet):
    queryset = models.PhoneBook.objects.all()
    serializer_class = serializers.PhonebookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
