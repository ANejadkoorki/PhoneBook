# Generated by Django 3.2.5 on 2021-07-15 06:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PhoneBook', '0002_phonebook_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonebook',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='phone number invalid', regex='^(\\+98?)?{?(0?9[0-9]{9,9}}?)$')], verbose_name='phone number'),
        ),
        migrations.AlterUniqueTogether(
            name='phonebook',
            unique_together={('phone_number', 'creator')},
        ),
    ]
