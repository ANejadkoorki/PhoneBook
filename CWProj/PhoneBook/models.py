from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

phone_regex = RegexValidator(regex='^(\+98?)?{?(0?9[0-9]{9,9}}?)$', message=_('phone number invalid'))


class PhoneBook(models.Model):
    # owner
    creator = models.ForeignKey('auth.User', verbose_name=_('creator'), on_delete=models.PROTECT, null=True)
    # Phone Book
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
    phone_number = models.CharField(validators=[phone_regex], max_length=11, verbose_name=_('phone number'))

    class Meta:
        unique_together = [
            'phone_number', 'creator'
        ]
        verbose_name = _('Phone Book')





