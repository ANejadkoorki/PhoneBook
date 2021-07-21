import json

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.http import JsonResponse

from PhoneBook.models import PhoneBook


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', )

    def handle(self, *args, **options):
        user = get_user_model().objects.get(username=options['username'])
        qs = PhoneBook.objects.filter(creator=user)
        json_data = {}
        for contact in qs:
            json_data[f'{contact.first_name} details'] = {
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'phone_number': contact.phone_number
            }
        with open(f'{user.username}_data.json', 'w') as handler:
            json.dump(json_data, handler)

        return f"json file of {user.username} created"
