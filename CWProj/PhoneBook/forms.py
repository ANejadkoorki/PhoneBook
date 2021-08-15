from django import forms
from django.core.validators import RegexValidator

from . import models

phone_regex = RegexValidator(regex='^(\+98?)?{?(0?9[0-9]{9,9}}?)$', message='phone number invalid')


class AddEntryForm(forms.ModelForm):
    class Meta:
        model = models.PhoneBook
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]


class SearchEntryForm(forms.Form):
    phone_number = forms.CharField(validators=[phone_regex], max_length=11)
    Choice = [
        ('exactly this number', 'exactly this number'),
        ('starts with this number', 'starts with this number'),
        ('ends with this number', 'ends with this number'),
        ('contains this number', 'contains this number'),
    ]
    search_mode = forms.ChoiceField(choices=Choice)
