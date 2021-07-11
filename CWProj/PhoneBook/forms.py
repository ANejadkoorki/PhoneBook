from django import forms

from . import models


class AddEntryForm(forms.ModelForm):
    class Meta:
        model = models.PhoneBook
        fields = [
            'first_name',
            'last_name',
            'phone_number',
        ]






