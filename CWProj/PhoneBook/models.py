from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

phone_regex = RegexValidator(regex='^(\+98?)?{?(0?9[0-9]{9,9}}?)$', message='phone number invalid')


class PhoneBook(models.Model):
    # owner
    creator = models.ForeignKey('auth.User', verbose_name='creator', on_delete=models.PROTECT, null=True)
    # Phone Book
    first_name = models.CharField(max_length=50, verbose_name='first name')
    last_name = models.CharField(max_length=50, verbose_name='last name')
    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name='phone number')

    class Meta:
        unique_together = [
            'phone_number', 'creator'
        ]

