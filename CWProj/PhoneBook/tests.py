from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from . import forms
from .forms import AddEntryForm
from .models import PhoneBook


class AddEntryTestCase(TestCase):
    def setUp(self):
        pass

    def test_page_rendering(self):
        response_for_login_required = self.client.get(reverse('PhoneBook:add-entry'))
        self.assertEqual(response_for_login_required.status_code, 302)
        response_for_page_rendering = self.client.get(reverse('PhoneBook:add-entry'), follow=True)
        self.assertEqual(response_for_page_rendering.status_code, 200)

    def test_post_transfer(self):
        data = {}
        resp = self.client.post(reverse('PhoneBook:add-entry'), data={
            'first_name': 'ahmad',
            'last_name': 'karimian',
            'phone_number': '09187456524',
        }, content_type='application/x-www-form-urlencoded')

        self.assertEqual(resp.status_code, 302)

    def test_valid_form(self):
        Entry = PhoneBook.objects.create(first_name='zahra', last_name='hassani', phone_number='09168745236')
        data = {'first_name': Entry.first_name, 'last_name': Entry.last_name, 'phone_number': Entry.phone_number}
        form = AddEntryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        Entry = PhoneBook.objects.create(first_name='zahra', last_name='hassani', phone_number='asdggsd')
        data = {'first_name': Entry.first_name, 'last_name': Entry.last_name, 'phone_number': Entry.phone_number}
        form = AddEntryForm(data=data)
        self.assertFalse(form.is_valid())


class SearchEntryTestCase(TestCase):
    def setUp(self):
        pass

    def test_rendered_page(self):
        resp = self.client.get(reverse('PhoneBook:search-entry'), follow=True)
        self.assertEqual(resp.status_code, 200)

        login = self.client.login(
            username='amirhossein',
            password='amir1381',
        )
        self.assertTrue(login)

        resp = self.client.get(reverse('PhoneBook:search-entry'), data={
            'phone_number': '09',
            'search_mode': 'contains this number'
        })
        self.assertEqual(resp.status_code, 302)


class ContactsTestCase(TestCase):
    def setUp(self):
        self.obj1 = PhoneBook.objects.create(first_name='amir', last_name='amiri', phone_number='09135247885')
        self.obj2 = PhoneBook.objects.create(first_name='ali', last_name='alavi', phone_number='09145247885')
        self.obj3 = PhoneBook.objects.create(first_name='karim', last_name='karimi', phone_number='09195247885')

    def test_qs_filtering(self):
        pass


class EditEntryTestCase(TestCase):
    def setUp(self):
        pass


class ActivitiesHistoryTestCase(TestCase):
    def setUp(self):
        pass
